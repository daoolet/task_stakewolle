from fastapi import FastAPI, Depends, Response, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import jwt

from .database import Base, engine, get_db
from .models import UserRepo, UserCreate


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
Base.metadata.create_all(bind=engine)

user_repo = UserRepo()


@app.get("/")
def root():
    return Response("OK", status_code=200)

# SIGNUP

@app.get("/signup")
def get_signup():
    return Response("Registered - OK", status_code=200)

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

def create_token(user_id: str) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "kek", "HS256")
    return token

def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "kek", "HS256")
    return data["user_id"]


@app.get("/login")
def get_login():
    return Response("OK", status_code=200)

@app.post("/login")
def post_login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_repo.get_by_email(db, user_email=data.username)
    if not user:
        return Response("Login is failed: Wrong email")
    
    if user.password == data.password:
        token = create_token(user.email)
    
    return {"access_token": token, "type": "bearer"}

# PROFILE

@app.get("/profile")
def get_profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    user = user_repo.get_by_id(db, user_id=user_id)
    return Response("Profile - OK", status_code=200)