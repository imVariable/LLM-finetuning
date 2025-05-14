Historical and analytical data for BTC, ETH, TSLA 
Filter by company or compare assets 
Generated metrics (7-day average, % change)
Summary generation using Groq LLM 
On demand data refresh 
Async FastAPI endpoints with Pydantic validation
Unit + integration test coverage 

Setup Instructions
1. Clone the repo 
2. Create and setup the virtual env 
3. Install dependencies 
pip install -r requirements.txt 
4. Setup the GROQ key 
5. Run the API server 
uvicorn app.main:app --reload