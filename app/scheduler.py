
from app.dao.products import get_all_trackings, add_tracking_record
from app.dao.schemas import PriceHistoryModel
from app.scraper import get_flipkart_product
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import time
import random
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

async def fetch_products_prices():
    """Fetch prices for all tracked products and store in history"""
    try:
        logger.info("Starting price fetch job...")
        products = await get_all_trackings()
        
        if not products:
            logger.info("No products to track")
            return
            
        logger.info(f"Found {len(products)} products to check")
        
        for product in products:
            try:
                # Add delay between requests to be respectful to the server
                await asyncio.sleep(random.uniform(2, 5))
                
                response = get_flipkart_product(product.get("url"))
                if response:
                    record = PriceHistoryModel(
                        product_id=ObjectId(product["product_id"]),
                        price=response["price"]
                    )
                    success = await add_tracking_record(record)
                    if success:
                        logger.info(f"Price recorded for {product.get('url')}: ₹{response['price']}")
                    else:
                        logger.error(f"Failed to insert price record for {product.get('name')}")
                else:
                    logger.warning(f"Could not fetch price for {product.get('url')}")
            except Exception as product_error:
                logger.error(f"Error processing product {product.get('url')}: {str(product_error)}")
                continue
                
        logger.info("Price fetch job completed")
    except Exception as e:
        logger.error(f"Error in fetch_products_prices: {str(e)}")


@asynccontextmanager
async def lifespan(app):
    """Manage app lifecycle: startup and shutdown"""
    # Setup: Start the scheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule the scraper to run every 30 minutes
    scheduler.add_job(fetch_products_prices, 'interval', hours=12, id='price_fetcher')
    
    try:
        scheduler.start()
        logger.info("🟢 Scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")
    
    yield
    
    # Shutdown
    try:
        scheduler.shutdown(wait=True)
        logger.info("Scheduler shutdown successfully")
    except Exception as e:
        logger.error(f"Error during scheduler shutdown: {str(e)}")
