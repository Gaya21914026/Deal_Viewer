from fastapi.encoders import jsonable_encoder
from bson import ObjectId

def create_template(db, template: dict):
    template = jsonable_encoder(template)

    result = db["template"].insert_one(template)
    created = db["template"].find_one({"_id": result.inserted_id})

    created["_id"] = str(created["_id"])

    return created

def get_all_templates(db):
    templates = list(db["template"].find({}))
    for t in templates:
        t["_id"] = str(t["_id"])
    return templates

def get_template_by_id(db, template_id: str):
    try:
        oid = ObjectId(template_id)
    except:
        return None  

    template = db["template"].find_one({"_id": oid})
    if template:
        template["_id"] = str(template["_id"])
    return template

def delete_template(db, template_id: str):
    try:
        oid = ObjectId(template_id)
    except:
        return "invalid_id"

    delete_result = db["template"].delete_one({"_id": oid})

    if delete_result.deleted_count == 1:
        return "deleted"

    return None


def update_template(db, template_id: str, template: dict):

    template = {k: v for k, v in template.items() if v is not None}

    try:
        oid = ObjectId(template_id)
    except:
        return "invalid_id"

    if len(template) >= 1:
        update_result = db["template"].update_one(
            {"_id": oid},
            {"$set": jsonable_encoder(template)}
        )
    else:
        return "empty"

    if update_result.modified_count == 0:
        return None  # pas trouvé

    # Récupérer le document mis à jour
    existing = db["template"].find_one({"_id": oid})
    if existing:
        existing["_id"] = str(existing["_id"])
        return existing

    return None
