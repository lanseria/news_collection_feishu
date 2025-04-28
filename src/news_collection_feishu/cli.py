import typer
from typing import Optional
import logging
from .fetch import fetch_latest_news, save_items, ensure_data_dir

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = typer.Typer()

@app.command()
def fetch_news():
    """Fetch latest news and save to daily file"""
    ensure_data_dir()
    
    logger.info("Fetching latest news...")
    result = fetch_latest_news()
    
    if not result or result.get('status') != 'success':
        logger.error("Failed to fetch news or invalid response")
        return
    
    items = result.get('items', [])
    if not items:
        logger.info("No items found in response")
        return
    
    save_items(items)
    logger.info("News fetch completed")

@app.command()
def hello(name: Optional[str] = typer.Argument(None)):
    """Simple greeting command"""
    if name:
        logger.info(f"Hello {name}!")
    else:
        logger.info("Hello World!")

if __name__ == "__main__":
    app()