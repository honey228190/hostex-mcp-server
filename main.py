import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

HOSTEX_TOKEN = os.getenv("HOSTEX_TOKEN", "")
BASE_URL = "https://api.hostex.io"
HEADERS = {
    "Authorization": f"Bearer {HOSTEX_TOKEN}",
    "Content-Type": "application/json"
}

# 根路径探活
@app.get("/")
def root():
    return {"status": "running", "service": "Hostex MCP Proxy"}

# 1. 获取房源日历
@app.post("/get_room_calendar")
async def get_room_calendar(request: Request):
    data = await request.json()
    room_id = data.get("room_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    url = f"{BASE_URL}/v1/calendar"
    params = {"room_id": room_id, "start_date": start_date, "end_date": end_date}
    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=10)
        return JSONResponse(status_code=res.status_code, content=res.json())
    except Exception as e:
        return {"error": str(e)}

# 2. 更新房源价格
@app.post("/update_hostex_price")
async def update_hostex_price(request: Request):
    data = await request.json()
    room_id = data.get("room_id")
    date = data.get("date")
    price = data.get("price")
    
    url = f"{BASE_URL}/v1/calendar/price"
    payload = {"room_id": str(room_id), "date": date, "price": price}
    try:
        res = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        return JSONResponse(status_code=res.status_code, content=res.json())
    except Exception as e:
        return {"error": str(e)}
