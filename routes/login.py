from datetime import datetime, timedelta
from typing import Annotated, List, Dict
from fastapi import Depends, APIRouter, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import bcrypt
from models.models import Token, TokenData, User, UserInDB, UserRegistration, News, myOpinion
from config.dbfull import db
from pymongo.collection import Collection

from schemas.schemas import UserPramuka

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

login = APIRouter(tags=["Login"])

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
    
):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_news(
news : News = Depends(get_current_user)

):
    if not news.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return news

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    user_dict = db.users.find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)
    else:
        return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def admin_required(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    return current_user

# Decorator untuk memeriksa apakah pengguna adalah non-admin
def non_admin_required(current_user: UserInDB = Depends(get_current_user)):
    if current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    return current_user

@login.post("/register", response_model=Dict[str, str])
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    is_admin: str = Form(...),
):
    if db.users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(password)
    if db.users.find_one({"email": "admin@admin.com"}):
        user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "hashed_password": hashed_password,
            "active": True,
            "is_admin": False
        }
    else:
        user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "hashed_password": hashed_password,
            "active": True,
            "is_admin": False
        }
    db.users.insert_one(user_data)

    return {"message": "User registered successfully"}

@login.post("/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = authenticate_user(username, password)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@login.get("/users/me/", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    # Query untuk mendapatkan data dari db.users berdasarkan username
    user_data = db.users.find_one({"username": current_user.username})

    # Membuat instance UserInDB
    user_in_db = UserInDB(
        full_name=user_data["full_name"],
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=user_data["hashed_password"],
        active=user_data["active"],
        is_admin=user_data["is_admin"],
    )

    # Query untuk mendapatkan data dari db.opinion berdasarkan sender_name yang sama dengan full_name user aktif
    opinions_cursor = db.opinion.find({"sender_name": user_in_db.full_name})

    # Mengisi atribut opinions pada user_in_db dengan data dari db.opinion
    user_in_db.opinions = [myOpinion(**opinion_data) for opinion_data in opinions_cursor]

    return user_in_db

@login.get('/user/all',dependencies=[Depends(admin_required)])
async def get_all_user():
    user_cursor = db.users.find()
    user_list = list(user_cursor)
    if not user_list:
        return []
    for user in user_list:
        for user in user_list:
            user["_id"] = str(user["_id"])
            user.setdefault("status", False)
    result = [UserPramuka(user) for user in user_list]
    return result