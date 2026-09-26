import os
import requests
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP 服务
mcp = FastMCP("Hostex Dynamic Pricing Agent")

# 从 Render 环境变量读取 Access Token
HOSTEX_TOKEN = os.getenv("HOSTEX_TOKEN", "")
BASE_URL = "https://api.hostex.io"

HEADERS = {
    "Authorization": f"Bearer {HOSTEX_TOKEN}",
    "Content-Type": "application/json"
}

@mcp.tool()
def get_room_calendar(room_id: str, start_date: str, end_date: str) -> str:
    """
    获取指定房源在某段时间内的日历状态（包括当前挂牌价、已预订/空置状态）。
    :param room_id: 房源/房型 ID
    :param start_date: 开始日期 YYYY-MM-DD
    :param end_date: 结束日期 YYYY-MM-DD
    """
    url = f"{BASE_URL}/v1/calendar"
    params = {"room_id": room_id, "start_date": start_date, "end_date": end_date}
    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if res.status_code == 200:
            return res.text
        return f"获取日历失败 ({res.status_code}): {res.text}"
    except Exception as e:
        return f"请求异常: {str(e)}"

@mcp.tool()
def update_hostex_price(room_id: str, date: str, price: float) -> str:
    """
    修改 Hostex 系统中指定房源在特定日期的挂牌价格（单位：日元）。
    :param room_id: 房源/房型 ID
    :param date: 修改日期的格式 YYYY-MM-DD
    :param price: 修改后的挂牌价格
    """
    url = f"{BASE_URL}/v1/calendar/price"
    payload = {
        "room_id": str(room_id),
        "date": date,
        "price": price
    }
    try:
        res = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return f"成功更新房源 {room_id} 在 {date} 的价格为 {price} 日元。"
        return f"修改失败，Hostex 返回状态码 {res.status_code}: {res.text}"
    except Exception as e:
        return f"请求异常: {str(e)}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(transport="sse")

