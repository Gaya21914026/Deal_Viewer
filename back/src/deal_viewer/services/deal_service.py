from datetime import UTC, datetime

from pymongo.errors import DuplicateKeyError
from deal_viewer.config.database import get_collection
from bson import ObjectId
from deal_viewer.models.deal_model import REQUIRED_FIELDS, CONTACT_FIELDS, AUTOMATIC_FIELDS

collection = get_collection("deals")
"insert le deal si il est conforme et retourne son id, sinon retourne l'erreur"
def insert_deal(deal: dict) -> str:

    try:
        result = collection.insert_one(deal)
        return str(result.inserted_id)

    except DuplicateKeyError:
        raise ValueError("Un deal avec cette référence existe déjà.")

    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'insertion du deal : {e}")

def get_all_deals() -> list:
    deals = list(collection.find({}))
    
    for deal in deals:
        deal["_id"] = str(deal["_id"])
    
    return deals

def get_deal_by_id(deal_id: str) -> dict:

    try:
        if not ObjectId.is_valid(deal_id):
            raise ValueError("ID invalide")
        
        deal = collection.find_one({"_id": ObjectId(deal_id)})

        if deal:
            deal["_id"] = str(deal["_id"])
        return deal

    except Exception as e:
        raise RuntimeError(f"Erreur lors de la récupération du deal : {e}")

def update_deal(deal_id: str, updates: dict) -> dict:

    if not ObjectId.is_valid(deal_id):
        raise ValueError("ID invalide")
    
    if (collection.find_one({"_id": ObjectId(deal_id)})) is None:
        return None

    if "_id" in updates:
        updates.pop("_id")
        
    if "updatedAt"  in updates:
        updates.pop("updatedAt")   

    updated_at= datetime.now(UTC)
    updates['Updated_at'] = updated_at

    result = collection.update_one(
        {"_id": ObjectId(deal_id)},
        {"$set": updates}
    )

    updated = collection.find_one({"_id": ObjectId(deal_id)})
    updated["_id"] = str(updated["_id"])
    return updated

def delete_deal(deal_id: str) -> bool:

    if not ObjectId.is_valid(deal_id):
        raise ValueError("ID invalide")
    
    result = collection.delete_one({"_id": ObjectId(deal_id)})

    if result.deleted_count == 0:
        raise ValueError("Deal non trouvé") 
    else:
        return True

def delete_fields(deal_id: str, fields: list[str]) -> dict:

    if not ObjectId.is_valid(deal_id):
        raise ValueError("ID invalide")

    deal = collection.find_one({"_id": ObjectId(deal_id)})
    if not deal:
        return None

    unset_fields = {}

    for field in fields:
        if field == "_id" or field in REQUIRED_FIELDS or field in CONTACT_FIELDS or field in AUTOMATIC_FIELDS or field=="updatedAt":
            continue  

        if field in deal:
            unset_fields[field] = ""

    
    if not unset_fields:
        return deal  

    
    collection.update_one(
        {"_id": ObjectId(deal_id)},
        {
            "$unset": unset_fields,
            "$set": {"updatedAt": datetime.now(UTC)}
        }
    )

    updated = collection.find_one({"_id": ObjectId(deal_id)})
    updated["_id"] = str(updated["_id"])
    return updated