from fastapi import APIRouter, Body, Request, status,HTTPException,Response
from deal_viewer.services.template_service import create_template,get_all_templates,get_template_by_id,delete_template,update_template

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.post("/", summary="Get all templates",status_code=status.HTTP_201_CREATED)
def create_template_route(request: Request, template: dict = Body(...)):
    return create_template(request.app.database, template)


@router.get("/", summary="Get all templates")
def get_templates_route(request: Request):
    return get_all_templates(request.app.database)


@router.get("/{template_id}", summary="Get template by ID")
def get_template_route(template_id: str, request: Request):
    template = get_template_by_id(request.app.database, template_id)

    if template is None:
        raise HTTPException(status_code=404, detail="Template non trouvé")

    return template


@router.delete("/{template_id}", summary="Delete a template by id")
def delete_template_route(template_id: str, request: Request, response: Response):
    result = delete_template(request.app.database, template_id)

    if result == "invalid_id":
        raise HTTPException(status_code=400, detail="ID invalide")

    if result == "deleted":
        return {"message": "Supprimé avec succès"}
        return response

    raise HTTPException(status_code=404, detail=f"Template avec ID {template_id} non trouvé")


@router.put("/{id}", response_description="Update template")
def update_template_route(id: str, request: Request, template: dict = Body(...)):
    result = update_template(request.app.database, id, template)

    if result == "invalid_id":
        raise HTTPException(status_code=400, detail="ID invalide")

    if result == "empty":
        raise HTTPException(status_code=400, detail="Aucune donnée à mettre à jour")

    if result is None:
        raise HTTPException(status_code=404, detail=f"Template avec ID {id} non trouvé")

    return result