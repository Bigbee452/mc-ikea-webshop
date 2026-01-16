from fastapi import FastAPI, Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

# --- ✅ Enable CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend URL: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database connection settings ---
DB_HOST = os.getenv("DB_HOST", "192.168.0.250")
DB_NAME = os.getenv("DB_NAME", "ikea")
DB_USER = os.getenv("DB_USER", "web_acces")
DB_PASS = os.getenv("DB_PASS", "0001")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# --- Product model ---
class Product(BaseModel):
    product_id: int
    name: str
    description: str | None = None
    price: float
    stock_quantity: int
    image_url: str | None = None

class Category(BaseModel):
    category_id: int
    name: str
    image_url: str | None = None

@app.get("/products")
def get_products(
    category: Optional[str] = Query(None),
):
    query = "SELECT product_id, products.name, price, stock_quantity, products.image_url FROM products "
    params = []

    if category:
        query += "JOIN categories ON categories.category_id=products.category_id WHERE categories.category_id = %s"
        params.append(f"{category}")
    else:
        query += "WHERE category_id IS NULL"
    query += " ORDER BY product_id;"

    # connect to database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "product_id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "stock_quantity": row[3],
            "image_url": row[4]
        }
        for row in rows
    ]

@app.get("/categories")
def get_categories():
    query = "SELECT category_id, name, image_url FROM categories"
    params = []

    query += " ORDER BY category_id;"

    # connect to database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "category_id": row[0],
            "name": row[1],
            "image_url": row[2]
        }
        for row in rows
    ]
