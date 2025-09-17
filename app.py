from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv
import os

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

# Simple in-memory user store (demo only; not for production)
class RegisterRequest(BaseModel):
    phone: str  # must be 10 digits
    password: str

class LoginRequest(BaseModel):
    phone: str
    password: str

class AuthResponse(BaseModel):
    token: str

users_store: dict[str, str] = {}  # phone -> password

# Utility validation
def validate_phone(phone: str):
    if not (phone.isdigit() and len(phone) == 10):
        raise HTTPException(status_code=400, detail="Phone must be a 10-digit number")

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
    if payload.phone in users_store:
        raise HTTPException(status_code=409, detail="User already exists")
    users_store[payload.phone] = payload.password
    # Issue a simple demo token
    token = f"demo-token-{payload.phone}"
    return {"token": token}

@app.post("/auth/login", response_model=AuthResponse)
async def login_user(payload: LoginRequest):
    validate_phone(payload.phone)
    if payload.phone not in users_store:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if users_store[payload.phone] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = f"demo-token-{payload.phone}"
    return {"token": token}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
