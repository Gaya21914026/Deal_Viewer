from fastapi import APIRouter, Body, HTTPException, Query
from deal_viewer.utils.deal_validator import validate_and_build_deal
from deal_viewer.services.deal_service import delete_fields, get_all_deals, insert_deal, get_deal_by_id, update_deal, delete_deal, get_filtered_deals


router = APIRouter(prefix="/deals", tags=["Deals"])


@router.post("/")
def create_deal(payload: dict):
    try:
        deal = validate_and_build_deal(payload)
        inserted_id = insert_deal(deal)
        return {
            "message": "Deal créé avec succès",
            "dealId": inserted_id
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")


@router.get("/")
def get_deals(
    clientName: str = Query(None),
    startDate: str = Query(None),
    endDate: str = Query(None)
):
    try:
        # Si des filtres sont fournis, les appliquer
        if clientName or startDate or endDate:
            deals = get_filtered_deals(clientName, startDate, endDate)
        else:
            deals = get_all_deals()
        
        return deals

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")
    

@router.get("/{deal_id}")
def get_one_deal(deal_id: str):
    try:
        deal = get_deal_by_id(deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail="Deal non trouvé")
        return deal
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")  


@router.put("/{deal_id}")
def update_deal_route(deal_id: str, updates: dict):
    try:
        updated = update_deal(deal_id, updates)

        if updated is None:
            raise HTTPException(status_code=404, detail="Deal non trouvé")

        return updated

    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalide")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")

@router.delete("/{deal_id}")
def delete_deal_route(deal_id: str):

    try:
        delete_deal(deal_id)
        return {"message": "Deal supprimé avec succès"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")
    
@router.put("/{deal_id}/fields")
def delete_field_(deal_id: str, fields: list[str]=Body(...)):
    try:
        updated = delete_fields(deal_id, fields)

        if updated is None:
            raise HTTPException(status_code=404, detail="Deal ou champ non trouvé")

        return updated

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")
    

    