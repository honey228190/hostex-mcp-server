import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 从环境变量中安全获取 Hostex 鉴权 Token
HOSTEX_TOKEN = os.getenv("HOSTEX_TOKEN", "")
BASE_URL = "https://open-api.hostex.io"  # 确保符合官方 API 域名

HEADERS = {
    "Authorization": f"Bearer {HOSTEX_TOKEN}",
    "Content-Type": "application/json"
}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hostex MCP & Pricing Server is running!"}

# 1. 获取房源列表
@app.get("/get_properties")
def get_properties():
    url = f"{BASE_URL}/v1/properties"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        return JSONResponse(status_code=res.status_code, content=res.json())
    except Exception as e:
        return {"error": str(e)}

# 2. 查询房源日历与价格（对齐官方 Listing Calendars POST 规范）
@app.post("/get_room_calendar")
async def get_room_calendar(request: Request):
    data = await request.json()
    room_id = data.get("room_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    # 官方标准的日历查询端点
    url = f"{BASE_URL}/v1/listing-calendars/query"
    payload = {
        "room_ids": [room_id],
        "start_date": start_date,
        "end_date": end_date
    }
    try:
        res = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        return JSONResponse(status_code=res.status_code, content=res.json())
    except Exception as e:
        return {"error": str(e)}

# 3. 更新房源价格（对齐官方 Update Listing Prices 规范）
@app.post("/update_hostex_price")
async def update_hostex_price(request: Request):
    data = await request.json()
    room_id = data.get("room_id")
    date = data.get("date")
    price = data.get("price")
    
    # 官方标准的改价端点
    url = f"{BASE_URL}/v1/listing-prices"
    payload = {
        "room_id": room_id,
        "date": date,
        "price": price
    }
    try:
        res = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        return JSONResponse(status_code=res.status_code, content=res.json())
    except Exception as e:
        return {"error": str(e)}
