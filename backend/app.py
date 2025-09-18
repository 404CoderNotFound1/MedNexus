from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv
import os
from sqlmodel import SQLModel, Field, Session, create_engine, select
from passlib.context import CryptContext

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup (SQLite)
DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DB_PATH, echo=False)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Admin secret for dev-only endpoints
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "devsecret")

# Sample data model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Sample database
items_db = [
    {"id": 1, "name": "First Item", "description": "This is the first item"},
    {"id": 2, "name": "Second Item", "description": "This is the second item"},
]

class RegisterRequest(BaseModel):
    phone: str  # must be 10 digits
    password: str

class LoginRequest(BaseModel):
    phone: str
    password: str

class AuthResponse(BaseModel):
    token: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str = Field(index=True, unique=True)
    password_hash: str

def validate_phone(phone: str):
    if not (phone.isdigit() and len(phone) == 10):
        raise HTTPException(status_code=400, detail="Phone must be a 10-digit number")

def get_session():
    with Session(engine) as session:
        yield session

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# API endpoints
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.get("/items", response_model=List[Item])
async def read_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Auth endpoints
@app.post("/auth/register", response_model=AuthResponse)
async def register_user(payload: RegisterRequest):
    validate_phone(payload.phone)
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.phone == payload.phone)).first()
        if existing:
            raise HTTPException(status_code=409, detail="User already exists")
        user = User(phone=payload.phone, password_hash=hash_password(payload.password))
        session.add(user)
        session.commit()
        session.refresh(user)
    token = f"demo-token-{payload.phone}"
    return {"token": token}

@app.post("/auth/login", response_model=AuthResponse)
async def login_user(payload: LoginRequest):
    validate_phone(payload.phone)
    with Session(engine) as session:
        user = session.exec(select(User).where(User.phone == payload.phone)).first()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    token = f"demo-token-{payload.phone}"
    return {"token": token}

# Dev-only admin endpoint to list registered users' phones
@app.get("/users")
async def list_users(x_admin_secret: str | None = Header(default=None, alias="X-Admin-Secret")):
    # Protect with an admin secret to avoid accidental exposure
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")
    with Session(engine) as session:
        rows = session.exec(select(User.phone)).all()
    return {"users": [{"phone": p} for p in rows]}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
