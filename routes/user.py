from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from models.models import UserRegistration
from config.dbfull import users_connection
import hashlib
import hmac
from jose import jwt, JWTError
import base64
from datetime import datetime, timedelta
from bson import json_util

SECRET_KEY = "your_secret_key"  # Ganti dengan kunci rahasia Anda
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

regist = APIRouter(tags=["Registrasi"])

# Function to hash password using HS256
def hash_password(password: str, secret_key: str) -> str:
    hashed = hmac.new(secret_key.encode('utf-8'), password.encode('utf-8'), hashlib.sha256)
    return base64.urlsafe_b64encode(hashed.digest()).decode('utf-8')

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = users_connection.local.users.find_one({"username": username})
    if user and verify_password(password, user["hashed_password"]):
        return user
    else:
        return None

# Function to verify password
def verify_password(plain_password, hashed_password):
    return hashed_password == hash_password(plain_password, SECRET_KEY)

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @regist.post("/", response_model=UserRegistration)
# async def register_user(user: UserRegistration):
#     # Cek apakah nama pengguna sudah terdaftar
#     if users_connection.local.users.find_one({"username": user.username}):
#         raise HTTPException(status_code=400, detail="Username already taken")

#     # Cek apakah email sudah terdaftar
#     if users_connection.local.users.find_one({"email": user.email}):
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Hash password menggunakan HS256
#     hashed_password = hash_password(user.hashed_password, SECRET_KEY)

#     # Simpan data pengguna ke database MongoDB
#     user_data = user.dict()
#     user_data["hashed_password"] = hashed_password
#     users_connection.local.users.insert_one(user_data)

#     return user

# @regist.post("/login")
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     username = form_data.username
#     password = form_data.password

#     user = authenticate_user(username, password)
#     if user:
#         access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
#         return {"access_token": access_token, "token_type": "bearer"}
#     else:
#         raise HTTPException(status_code=401, detail="Invalid credentials")