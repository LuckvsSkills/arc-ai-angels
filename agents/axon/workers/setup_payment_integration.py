#!/usr/bin/env python3
"""
setup_payment_integration.py — Axon worker
Configureert Stripe payment integratie op basis van PROJECT_BRIEF.json
Gebruik: python3 setup_payment_integration.py /pad/naar/PROJECT_BRIEF.json
"""
import os, sys, json
from datetime import datetime

STRIPE_TYPES = {
    'ecommerce':   'checkout',
    'saas':        'subscriptions',
    'marketplace': 'connect',
    'booking':     'checkout',
    'community':   'subscriptions',
}

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def load_brief(path):
    with open(path) as f:
        return json.load(f)

def setup_stripe(brief, project_dir):
    ptype = brief['type']
    stripe_type = STRIPE_TYPES.get(ptype)
    if not stripe_type:
        log(f'ℹ️  Type {ptype} heeft geen Stripe integratie nodig')
        return None
    code_dir = brief.get('code_dir', f'{project_dir}/code')
    backend_dir = f'{code_dir}/backend'
    os.makedirs(backend_dir, exist_ok=True)

    # .env.example aanmaken
    env_path = f'{code_dir}/.env.example'
    env_content = f"""# {brief['project_naam']} — Environment Variables
# Kopieer naar .env en vul in

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
"""
    if stripe_type == 'connect':
        env_content += "STRIPE_CLIENT_ID=ca_...\n"
    with open(env_path, 'w') as f:
        f.write(env_content)

    # Stripe payment module aanmaken
    stripe_module = f'{backend_dir}/stripe_payments.py'
    if stripe_type == 'checkout':
        code = f'''"""
Stripe Checkout integratie — {brief['project_naam']}
"""
import os
import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
router = APIRouter()

class CheckoutRequest(BaseModel):
    product_naam: str
    prijs_cents: int
    success_url: str = "https://{brief.get('domein', 'example.com')}/success"
    cancel_url: str = "https://{brief.get('domein', 'example.com')}/cancel"

@router.post("/api/checkout")
async def create_checkout(req: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "ideal"],
            line_items=[{{
                "price_data": {{
                    "currency": "eur",
                    "product_data": {{"name": req.product_naam}},
                    "unit_amount": req.prijs_cents,
                }},
                "quantity": 1,
            }}],
            mode="payment",
            success_url=req.success_url,
            cancel_url=req.cancel_url,
        )
        return {{"checkout_url": session.url, "session_id": session.id}}
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/api/webhook/stripe")
async def stripe_webhook(request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, os.getenv("STRIPE_WEBHOOK_SECRET", ""))
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            # TODO: order verwerken
            print(f"Betaling ontvangen: {{session['id']}}")
        return {{"status": "ok"}}
    except Exception as e:
        raise HTTPException(400, str(e))
'''
    elif stripe_type == 'subscriptions':
        code = f'''"""
Stripe Subscriptions integratie — {brief['project_naam']}
"""
import os
import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
router = APIRouter()

class SubscriptionRequest(BaseModel):
    email: str
    price_id: str
    success_url: str = "https://{brief.get('domein', 'example.com')}/dashboard"
    cancel_url: str = "https://{brief.get('domein', 'example.com')}/pricing"

@router.post("/api/subscribe")
async def create_subscription(req: SubscriptionRequest):
    try:
        customer = stripe.Customer.create(email=req.email)
        session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=["card"],
            line_items=[{{"price": req.price_id, "quantity": 1}}],
            mode="subscription",
            success_url=req.success_url,
            cancel_url=req.cancel_url,
        )
        return {{"checkout_url": session.url}}
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/api/webhook/stripe")
async def stripe_webhook(request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, os.getenv("STRIPE_WEBHOOK_SECRET", ""))
        if event["type"] == "customer.subscription.created":
            print(f"Nieuw abonnement: {{event['data']['object']['id']}}")
        elif event["type"] == "customer.subscription.deleted":
            print(f"Abonnement opgezegd: {{event['data']['object']['id']}}")
        return {{"status": "ok"}}
    except Exception as e:
        raise HTTPException(400, str(e))
'''
    else:
        code = f'# Stripe Connect integratie voor {brief["project_naam"]}\n# TODO: implementeren\n'

    with open(stripe_module, 'w') as f:
        f.write(code)

    log(f'✅ Stripe {stripe_type} module aangemaakt: {stripe_module}')
    log(f'✅ .env.example aangemaakt: {env_path}')
    return stripe_type

def update_brief(brief_path, brief, stripe_type):
    brief['payment'] = {
        'provider': 'stripe',
        'type': stripe_type,
        'configured_at': datetime.now().isoformat(),
        'test_mode': True
    }
    brief['sentinels']['axon'] = 'DONE'
    with open(brief_path, 'w') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 setup_payment_integration.py /pad/naar/PROJECT_BRIEF.json')
        sys.exit(1)
    brief_path = sys.argv[1]
    brief = load_brief(brief_path)
    project_dir = os.path.dirname(brief_path)
    log(f'💳 Payment integratie: {brief["project_naam"]} ({brief["type"]})')
    stripe_type = setup_stripe(brief, project_dir)
    if stripe_type:
        update_brief(brief_path, brief, stripe_type)
        print('\n' + '='*50)
        print('✅ AXON PAYMENT KLAAR')
        print(f'   Provider: Stripe {stripe_type}')
        print(f'   Mode: TEST (niet productie)')
        print(f'   Volgende: Nero security scan')
        print('='*50)
    else:
        print('ℹ️  Geen payment integratie vereist')

if __name__ == '__main__':
    main()
