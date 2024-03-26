from fastapi import FastAPI, Depends, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import jwt

from random import choice
from string import ascii_letters, digits
from datetime import datetime, timedelta


from .database import Base, engine, get_db
from .models import UserRepo
from .schemas import UserCreate


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
Base.metadata.create_all(bind=engine)

user_repo = UserRepo()


@app.get("/")
def root():
    return Response("OK", status_code=200)

# SIGNUP

@app.post("/signup")
def post_signup(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = user_repo.get_by_email(db, user_email=email)
    if user:
        raise HTTPException(detail="User already exists with this email", status_code=400)
    
    new_user = UserCreate(email=email, password=password)
    answer = user_repo.save_user(db, user=new_user)
    return answer


# LOGIN

def create_access_token(user_email: str) -> str:
    body = {"user_email": user_email}
    token = jwt.encode(body, "kek", "HS256")
    return token

def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "kek", "HS256")
    return data["user_email"]

@app.post("/login")
def post_login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_repo.get_by_email(db, user_email=data.username)
    if not user:
        return Response("Login is failed: Wrong email")
    
    if user.password == data.password:
        token = create_access_token(user.email)
    
    return {"access_token": token, "type": "bearer"}


# PROFILE

@app.get("/profile")
def get_profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_email = decode_jwt(token)
    user = user_repo.get_by_email(db, user_email=user_email)

    content = {
        "user_id": user.id,
        "user_email": user.email,
        "referral_code": user.referral_code,
        "ref_code_is_active": user.ref_code_is_active,
        "ref_code_created_ad": user.ref_code_created_at,
        "ref_code_expiry_date": user.ref_code_expiry_date
    }

    if user.ref_code_created_at:
        content["ref_code_created_ad"] = user.ref_code_created_at.isoformat()
    else:
        content["ref_code_created_ad"] = None

    if user.ref_code_expiry_date:
        content["ref_code_expiry_date"] = user.ref_code_expiry_date.isoformat()
    else:
        content["ref_code_expiry_date"] = None

    return JSONResponse(content)


@app.get("/referral_code")
def get_referral_code(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    length: int = 10,
    expiry_day: int = 30
):
    user_email = decode_jwt(token)
    user = user_repo.get_by_email(db, user_email=user_email)

    characters = ascii_letters + digits
    referral_code = ''.join(choice(characters) for _ in range(length))

    if not user.ref_code_is_active:
        user.referral_code = referral_code
        user.ref_code_created_at = datetime.now()
        user.ref_code_is_active = True
        user.ref_code_expiry_date = user.ref_code_created_at + timedelta(days=expiry_day)

        context = {
            "referral code": user.referral_code,
            "is active": user.ref_code_is_active,
            "created at": user.ref_code_created_at.isoformat(),
            "expires on": user.ref_code_expiry_date.isoformat()
        }
    else:
        context = {
            "detail": f"Your {user.referral_code} - referral code is still active"
        }

    db.commit()
    return JSONResponse(context)

    

