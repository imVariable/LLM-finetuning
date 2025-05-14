from groq import Groq 
import yfinance as yf 
import os 
import pandas as pd 
from typing import List, Optional 
from fastapi import HTTPException 
from ..services.data_loader import fetch_asset_data 

os.environ['GROQ_API_KEY'] = ""

df = fetch_asset_data()

def filtered_data(
    company: Optional[str]=None, 
    companies: Optional[List[str]]=None 
):
    try:
        data = df.copy()
        if company:
            data = data[data['Company'].str.upper() == company.upper()]
        if companies:
            data = data[
                    data['Company'].str.upper().isin([c.upper() for c in companies])
                ]
        if data.empty:
            return []
        data = data.fillna("").reset_index()
        for col in data.select_dtypes(include=['datetime64[ns]']):
            data[col]=data[col].astype(str)
            
        return data.to_dict(orient="records")
    
    except Exception as e:
        raise RuntimeError(
            f"Data filtering failed: {str(e)}"
        )
        
def ingest_new_data(data: list):
    global df 
    try:
        new_df = pd.DataFrame(data)
        
        required_cols = [
            "Date",
            "Open",
            "High",
            "Low",
            "Volume",
            "Dividends",
            "Stock Splits",
            "Company",
            "Latest Price",
            "Average_ClosingPrice_7d",
            "Closing_change_percent_24h",
        ]
        if not required_cols.issubset(new_df.columns):
            raise HTTPException(
                status_code = 400,
                detail = f"Missing required columns. Required: {required_cols}",
            )
            
        if "Date" in new_df.columns:
            new_df['Date']=pd.to_datetime(
                new_df['Date'],
                errors="coerce"
            )
        df = pd.concat(
            [df, new_df],
            ignore_index = True 
        )
        return {
            "message": "Data ingested successfully",
            "records":len(new_df)
        }
        
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail=str(e)
        )
        
def get_summary_response():
    data_sample = (
        df[
            [
                "Company",
                "Latest Price",
                "Closing_change_percent_24h",
                "Average_ClosingPrice_7d",
            ]
        ]
        .drop_duplicates()
        .reset_index()
    )
    
    client = Groq(api_key = os.environ['GROQ_API_KEY'])
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes tabular or json data."
        },
        {
            "role": "user",
            "content": f"Summarize the data in 100 words and don't add anything of your own: \n{data_sample}"
        }
    ]
    completion = client.chat.completions.create(
        model = "meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature = 0.3,
        max_completions_token = 1024,
        top_p=1,
        stream = True,
        stop=None,
    )
    
    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""
    return {
        "Summary" : result
    }