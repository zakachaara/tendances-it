from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class OrderQuery(BaseModel):
    order_id: str

# Mock database
ORDERS = {
    "ORD123": {"status": "Shipped", "delivery": "2 days", "tracking": "TRK789"},
    "ORD456": {"status": "Processing", "delivery": "5 days", "tracking": "N/A"},
    "ORD789": {"status": "Delivered", "delivery": "Delivered yesterday", "tracking": "TRK101"}
}

REFUND_POLICIES = {
    "window": "30 days",
    "conditions": "Product must be unused and in original packaging"
}

@app.post("/tools/get_order_status")
def get_order_status(query: OrderQuery):
    order = ORDERS.get(query.order_id, {
        "status": "Not Found",
        "delivery": "N/A",
        "tracking": "N/A"
    })
    return order

@app.get("/tools/get_refund_policy")
def get_refund_policy():
    return REFUND_POLICIES

@app.get("/health")
def health():
    return {"status": "healthy"}
