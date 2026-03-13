from fastapi import APIRouter, Body, Request, status
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import json
from bson import ObjectId
from deal_viewer.services.deal_service import get_all_deals
from deal_viewer.services.template_service import get_template_by_name

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_json(template_name: str,request: Request):
    data = get_all_deals()
    template = get_template_by_name(request.app.database,template_name)
    visibleFields = template["visibleFields"]
    
    new_list = []

    for deal in data:  
        newobj = {}

        for field in visibleFields:
            if "." in field:
                fields = field.split(".")  
                if fields[0] in deal and fields[1] in deal[fields[0]]:
                    newobj[field] = deal[fields[0]][fields[1]]

            else:
                if field in deal:
                    newobj[field] = deal[field]

        new_list.append(newobj)

    return new_list
   



# @router.post("/", response_description="Get deal", status_code=status.HTTP_201_CREATED)
# async def upload_json(template_name:str):

    # try:
        # Read file contents
        # contents = get_all_deals()
        # 1 - recuperer le nom du template 
        # 2 - recupère depuis ta db 
        # template=get_template_by_name(template_name)
        # 3 - recup visibleFields
        # visibleFields = template["visibleFields"]
        # 4 Parcourir le deals et recupèrer les éléments qui sont dans visibleFields
        # Parse JSON
        # print(visibleFields)
        

    #     newobj = {}
    #     for field in visibleFields: 
    #         if field.__contains__("."):
    #             fields = field.split('.')
    #             if field in data and data[field] is not None:
    #                 newobj[field] = data[fields[0]][fields[1]]
            

    #     deal = jsonable_encoder(newobj)

    #     # new_deal = request.app.database["deal"].insert_one(data)
             
    #     return JSONResponse(content={
    #         "filename": file.filename,
    #         "filteredDeal": newobj,
    #         "inserted_id": str(deal)
    #     })

    # except json.JSONDecodeError:
    #     raise HTTPException(status_code=400, detail="Invalid JSON format")

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))








        # data_search = {k: v for k, v in data.items() if v is True}
        # if len(data_search) > 0:
        #     data_search_result = request.app.database["template"].insert_one(
        #     {data_search}   
        # )    
            
        # if data_search:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="template with ID id not found") 
        
        # Example: return parsed JSON back to client
    #     return JSONResponse(content={"filename": file.filename, "data": data})

    # except json.JSONDecodeError:
    #     raise HTTPException(status_code=400, detail="Invalid JSON format")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


# @router.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}


# @router.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
    # return {"filename": file.filename}

# @router.post("/", response_description="Get deal", status_code=status.HTTP_201_CREATED)
# def create_book(request: Request, deal = Body(...)):
#     deal = jsonable_encoder(deal)
#     new_deal = request.app.database["deal"].insert_one(deal)
#     insert_deal = request.app.database["deal"].find_one(
#         {"_id": new_deal.inserted_id}
#     )

#     return insert_deal
