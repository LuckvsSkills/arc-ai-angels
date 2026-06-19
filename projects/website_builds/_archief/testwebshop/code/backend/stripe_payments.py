"""
Stripe Checkout integratie — TestWebshop
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
    success_url: str = "https://testwebshop.vercel.app/success"
    cancel_url: str = "https://testwebshop.vercel.app/cancel"

@router.post("/api/checkout")
async def create_checkout(req: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card", "ideal"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": req.product_naam},
                    "unit_amount": req.prijs_cents,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=req.success_url,
            cancel_url=req.cancel_url,
        )
        return {"checkout_url": session.url, "session_id": session.id}
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
            print(f"Betaling ontvangen: {session['id']}")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(400, str(e))
