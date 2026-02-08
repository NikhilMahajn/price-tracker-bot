from app.dao.db_config import product_collection,user_product_collection,price_history_collection
from app.dao.schemas import PriceHistoryModel
from app.scraper import get_flipkart_product
from datetime import datetime
from bson.objectid import ObjectId

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
        prodcut = get_flipkart_product(url)
        user_product = {
            "user_id": user["id"],
            "product_id": product_id,
            "initial_price":int(prodcut["price"]),   
            "target_price": None,
            "product_name":prodcut["title"],
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

async def untrack_product(user,product_id):
    try:
        track_record = await user_product_collection.find_one({
                    "user_id": user["id"],
                    "product_id": ObjectId(product_id)
                    })
        
        prouct_name = ""
        if track_record:
            prouct_name = track_record["product_name"]
            await user_product_collection.delete_one({
                    "user_id": user["id"],
                    "product_id": ObjectId(product_id)
                    })
            
        # Delete from product if No Prodcut tracking is active for the product
        product_exits = await user_product_collection.find_one({"product_id": ObjectId(product_id)})
        
        if not product_exits:
            await product_collection.delete_one({"_id": ObjectId(product_id)})
            
        return {
                "status": "success",
                "message": "Product tracking removed",
                "product_id": str(product_id),
                "product_name":prouct_name
            }
    except Exception as e:
        print(str(e))
        return {
            "status": "failed",
            "message": "Product untracking failed",
            "product_id": str(product_id)
            
        }
        
async def get_all_trackings():
    trackings = user_product_collection.find()
    product_list = []
    async for track in trackings:
        producut = await product_collection.find_one({"_id": track["product_id"]})
        product_list.append(track|producut)
    return product_list


async def add_tracking_record(record: PriceHistoryModel):
    print("Adding record")
    try:
        # Option 1: Manually create a dictionary
        data = {
            "product_id": record.product_id,
            "price": record.price,
            "timestamp": datetime.utcnow() # Good practice to add a timestamp
        }
        
        result = await price_history_collection.insert_one(data)
        return result.inserted_id
        
    except Exception as e:
        print(f"Error inserting price record: {e}")
        return None
    