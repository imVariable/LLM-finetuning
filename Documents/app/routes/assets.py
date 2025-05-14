from fastapi import APIRouter, Query, HTTPException, Request 
from ..services.data_loader import fetch_asset_data 
from ..services.data_store import df as shared_df 

from ..services.data_service import (
    get_filtered_data,
    ingest_new_data,
    get_summary_response,
)

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)

@router.get("/")
async def get_all_assets():
    try:
        return get_filtered_data()
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail=str(e)
        )
        
@router.post("/refresh")
async def refresh_data():
    try:
        new_df = fetch_asset_data()
        from ..services import data_store 
        data_store.df = new_df 
        return {
            "message":"Data refreshed successfully.",
            "records": len(new_df)
        }
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Data refresh failed: {str(e)}"
        )
        
@router.get("/metrics/{company}")
async def get_company_metrics(company: str):
    try:
        result = get_filtered_data(company=company)
        if not result:
            raise HTTPException(
                status_code = 404,
                detail = "Company not found"
            )
        return result 
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail=str(e)
        )
        
@router.get("/ingest")
async def ingest_assets(request: Request):
    try:
        data = await request.json()
        return ingest_new_data(data)
    except Exception as e:
        raise HTTPException(
            status_code = 400,
            detail = str(e)
        )
        
@router.get("/summary")
async def summary():
    try: 
        return get_summary_response()
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )
        
        