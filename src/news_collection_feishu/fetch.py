from typing import Optional, List, Dict
import logging
import requests
from datetime import datetime, date
import json
from pathlib import Path

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configuration
API_URL = "https://newsnow.busiyi.world/api/s?id=ithome&latest"
HEADERS = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE0ODAyNzY0IiwidHlwZSI6ImdpdGh1YiIsImV4cCI6MTc1MDYzODgwMX0.UNILbo4iqjbETQ6UdlCwF0-6UzzaQpFVuwAiu9a7XDY",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://newsnow.busiyi.world/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
COOKIES = {
    "_ga": "GA1.1.100690081.1738732099",
    "_ga_EL9HHYE5LC": "GS1.1.1745823449.217.0.1745823449.0.0.0"
}
DATA_DIR = Path("news_data")

def ensure_data_dir():
    """Ensure the data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_today_filename() -> Path:
    """Get filename for today's data"""
    today = date.today().isoformat()
    return DATA_DIR / f"{today}.json"

def load_existing_items() -> Dict[str, List[Dict]]:
    """Load existing items from today's file if it exists"""
    today_file = get_today_filename()
    if not today_file.exists():
        return {}
    
    try:
        with open(today_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {item['id']: item for item in data.get('items', [])}
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading existing items: {e}")
        return {}

def fetch_latest_news() -> Optional[Dict]:
    """Fetch latest news from the API"""
    try:
        response = requests.get(
            API_URL,
            headers=HEADERS,
            cookies=COOKIES,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return None

def save_items(new_items: List[Dict]):
    """Save items to today's file, handling duplicates"""
    today_file = get_today_filename()
    existing_items = load_existing_items()
    
    # Filter out duplicates
    unique_new_items = [
        item for item in new_items 
        if item['id'] not in existing_items
    ]
    
    if not unique_new_items:
        logger.info("No new items to save")
        return
    
    # Combine existing and new items
    all_items = list(existing_items.values()) + unique_new_items
    
    # Sort by pubDate (newest first)
    all_items.sort(
        key=lambda x: datetime.strptime(x['pubDate'], "%Y-%m-%d %H:%M:%S"),
        reverse=True
    )
    
    data = {
        "status": "success",
        "updatedTime": datetime.now().timestamp() * 1000,
        "items": all_items
    }
    
    try:
        with open(today_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(unique_new_items)} new items to {today_file}")
    except IOError as e:
        logger.error(f"Error saving items: {e}")
