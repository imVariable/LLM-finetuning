from pydantic import BaseModel, Field 
from typing import Optional 
from datetime import datetime 

class AssetRecordO(BaseModel):
    Open: float 
    Close: float 
    High: float 
    Low: float 
    Volume: float 
    Dividends: float 
    Stock_splits : float = Field(..., alias = 'Stock Splits')
    Company: str 
    Latest_Price: Optional[float]=None 
    Average_ClosingPrice_7d: Optional[float]=None 
    Closing_change_percent_24h: Optional[float]=None 
    Date: Optional[datetime]=None 