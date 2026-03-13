from fastapi import APIRouter, Request, status
from deal_viewer.services.deal_service import get_all_deals
from deal_viewer.services.template_service import get_template_by_name

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_json(template_name: str, request: Request):
    deals = get_all_deals()  
    template = get_template_by_name(request.app.database, template_name)

    sections = template["sections"]
    labels = template.get("labels", {})
    visibleFields = template["visibleFields"]
    final_result = []

    for deal in deals:
        deal_output = []

        for section in sections:
            section_name = section["name"]
            fields = section["fields"]

            section_fields = {}

            for field in fields:
                value = None
                if "." in field:
                    splited = field.split(".")

                    if splited[0] in deal and splited[1] in deal[splited[0]]:
                        value = deal[splited[0]][splited[1]]


                else:
                    if field in deal:
                        value = deal[field]

                label = labels.get(field, field)

                section_fields[label] = value

            deal_output.append({
                "section": section_name,
                "fields": section_fields
            })

        label_values = {}

        for field in visibleFields:
            value = None

            if "." in field:
                parent, child = field.split(".")
                if parent in deal and child in deal[parent]:
                    value = deal[parent][child]
            else:
                if field in deal:
                    value = deal[field]

            if value is not None:
                label_values[field] = value

        deal_output.append({
            "labels": label_values
        })

        final_result.append(deal_output)

    return final_result



