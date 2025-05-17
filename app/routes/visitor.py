"""
visitor_router.py

This module implements visitor tracking APIs using FastAPI.

Features:
- Registers visitors via a unique visitor ID sent in the `X-Visitor-ID` header.
- Updates the visitor's last visited timestamp on repeat visits.
- Tracks total unique visitors globally.
- Returns the current count of unique visitors.

Endpoints:
/visit (POST):
    Registers or updates a visitor using the provided visitor ID header.
/count (GET):
    Retrieves the total count of unique visitors.

Dependencies:
- MongoDB database accessed via dependency injection (`get_db`).
- Standard datetime with timezone support for UTC timestamps.

Usage:
- Send POST /visit requests with header "X-Visitor-ID" to register or update visits.
- Query GET /count to get the total unique visitor count.
"""

from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Header, HTTPException
from app.dependencies import get_db

router = APIRouter()

@router.post("/visit")
async def register_visit(
    visitor_id: Optional[str] = Header(None, alias="X-Visitor-ID"),
    db=Depends(get_db)
):
    """
    Register a visitor's visit or update the timestamp if visitor already exists.

    Args:
        visitor_id (str, optional): Unique visitor ID from header 'X-Visitor-ID'. Required.
        db: Database session dependency.

    Raises:
        HTTPException: 400 error if 'X-Visitor-ID' header is missing.

    Returns:
        dict: Status message about visit registration or update.
    """

    if not visitor_id:
        raise HTTPException(status_code=400, detail="Missing X-Visitor-ID header")

    existing = await db.visitor.find_one({"_id": visitor_id})

    if existing:
        # Update last visited timestamp
        await db.visitor.update_one(
            {"_id": visitor_id},
            {"$set": {"visited_at": datetime.now(timezone.utc)
            }}
        )
        return {"message": "Visitor timestamp updated"}

    # New visitor: insert record with timestamp and increment global count
    await db.visitor.insert_one({"_id": visitor_id, "visited_at": datetime.now(timezone.utc)})

    await db.visitor.update_one(
        {"_id": "global"},
        {"$inc": {"count": 1}},
        upsert=True
    )
    return {"message": "Visit registered"}


@router.get("/count")
async def get_visit_count(db=Depends(get_db)):

    """
    Get the total count of unique visitors.

    Args:
        db: Database session dependency.

    Returns:
        dict: JSON object containing the total unique visitor count.
    """

    doc = await db.visitor.find_one({"_id": "global"})
    return {"count": doc["count"] if doc else 0}
