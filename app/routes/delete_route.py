"""
delete_route.py

This module defines API endpoints for deleting summarization records.

Features:
- DELETE all summaries.
- DELETE summaries associated with a specific visitor ID.

Dependencies:
- FastAPI for routing and dependency injection.
- MongoDB dependency via get_db.

Usage:
- DELETE /api/summaries/delete-all → Deletes all summaries.
- DELETE /api/summaries/delete-by-visitor?visitor_id=abc → Deletes summaries by visitor ID.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies import get_db

router = APIRouter()

@router.delete("/summaries/delete-all")
async def delete_all_summaries(db=Depends(get_db)):
    """
    Delete all summaries from the database.

    Returns:
        dict: Count of deleted documents.
    """
    result = await db.summaries.delete_many({})
    return {"deleted_count": result.deleted_count}


@router.delete("/summaries/delete-by-visitor")
async def delete_summaries_by_visitor(visitor_id: str = Query(..., description="Visitor ID to filter deletions"), db=Depends(get_db)):
    """
    Delete all summaries associated with a specific visitor ID.

    Args:
        visitor_id (str): Visitor identifier.

    Returns:
        dict: Count of deleted documents.
    """
    result = await db.summaries.delete_many({"visitor_id": visitor_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No summaries found for the given visitor ID.")
    return {"deleted_count": result.deleted_count}
