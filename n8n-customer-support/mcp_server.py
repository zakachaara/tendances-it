from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import random

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

SUPPORT_TICKETS = {}  # In-memory ticket storage

class TicketRequest(BaseModel):
    user_id: str
    issue_type: str
    description: str
    priority: str = "MEDIUM"

@app.post("/tools/create_support_ticket")
def create_support_ticket(ticket: TicketRequest):
    ticket_id = f"TKT{random.randint(10000, 99999)}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "user_id": ticket.user_id,
        "issue_type": ticket.issue_type,
        "description": ticket.description,
        "priority": ticket.priority,
        "status": "OPEN",
        "created_at": datetime.now().isoformat(),
        "estimated_response": "24 hours"
    }
    
    SUPPORT_TICKETS[ticket_id] = ticket_data
    
    return {
        "success": True,
        "ticket_id": ticket_id,
        "message": f"Support ticket {ticket_id} created successfully",
        "estimated_response": "24 hours"
    }

@app.get("/tools/get_ticket/{ticket_id}")
def get_ticket(ticket_id: str):
    ticket = SUPPORT_TICKETS.get(ticket_id)
    if ticket:
        return ticket
    return {"error": "Ticket not found"}

@app.get("/tools/list_tickets")
def list_tickets():
    return {"tickets": list(SUPPORT_TICKETS.values())}
    
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
