from fastapi import APIRouter, Request, status
from deal_viewer.services.deal_service import get_all_deals_projection
from deal_viewer.services.template_service import get_template_by_name
from deal_viewer.controllers.get_deal_adapter import DealTemplateAdapter

router = APIRouter()

@router.get("/")
async def upload_json(template_name: str, request: Request):
    template = get_template_by_name(request.app.database, template_name)

    projection = DealTemplateAdapter.build_projection(template)

    deals = get_all_deals_projection(request.app.database, projection)

    return DealTemplateAdapter.apply_template(deals, template)
