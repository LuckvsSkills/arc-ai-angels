from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
import os, jwt
from datetime import datetime, timedelta

router = APIRouter()

JWT_SECRET = os.environ.get("JWT_SECRET", "arc-ai-angels-secret-2026")
MCC_PASSWORD = os.environ.get("MCC_PASSWORD", "ArcAngels2026!")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://arc-vortex.nl")

def create_jwt(email):
    return jwt.encode({"sub": email, "exp": datetime.utcnow() + timedelta(days=30)}, JWT_SECRET, algorithm="HS256")

def verify_jwt(token):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

@router.get("/auth/login")
async def login():
    return {"url": None, "message": "Gebruik wachtwoord login"}

@router.post("/auth/login")
async def login_password(request: Request, response: Response):
    body = await request.json()
    password = body.get("password", "")
    if password != MCC_PASSWORD:
        raise HTTPException(401, "Ongeldig wachtwoord")
    token = create_jwt("fea@arc-ai-angels.nl")
    response.set_cookie("mcc_token", token, max_age=86400*30, httponly=True, samesite="lax")
    return {"ok": True, "email": "fea@arc-ai-angels.nl"}

@router.get("/auth/me")
async def get_me(request: Request):
    token = request.cookies.get("mcc_token")
    if not token:
        raise HTTPException(401, "Niet ingelogd")
    try:
        payload = verify_jwt(token)
        return {"ok": True, "email": payload.get("sub"), "logged_in": True}
    except:
        raise HTTPException(401, "Token verlopen")

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("mcc_token")
    return {"ok": True}
