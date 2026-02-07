from app.dao.db_config import product_collection,user_product_collection
from app.scraper import get_flipkart_price
from datetime import datetime

async def createProduct(url,platform):
    try:
        product = await product_collection.find_one({"url": url})
        if not product:
            product_data = {
				"platform": platform,
				"url": url,
				"created_at": datetime.utcnow()
			}
            result = await product_collection.insert_one(product_data)
            product_id = result.inserted_id
            
        else: 
            product_id = product["_id"]
        return product_id
    except Exception as e:
        print( "Error creating product",str(e))
        return None
    
async def track_product(user,product_id,url):
    try:
        exits = await user_product_collection.find_one({
                "user_id": user["id"],
                "product_id": product_id
                })
        if exits:
            return  {
            "status": "failed",
            "message":"product is already being tracked",
            "product_id": str(product_id),
        } 
        price = get_flipkart_price(url)
        user_product = {
            "user_id": user["id"],
            "product_id": product_id,
            "initial_price":int(price),   
            "target_price": None,
            "is_tracking": True,
            "created_at": datetime.utcnow()
        }

        await user_product_collection.insert_one(user_product)

        return {
            "status": "success",
            "message": "Product tracking started",
            "product_id": str(product_id),
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "Product tracking failed",
            "product_id": str(product_id),
        }

async def getUserProducts(user):
    producuts = user_product_collection.find({"user_id": user["id"]})
    product_list = []
    
    async for user_product in producuts:
        producut = await product_collection.find_one({"_id": user_product["product_id"]})
        product_list.append(user_product|producut)
        
    return product_list