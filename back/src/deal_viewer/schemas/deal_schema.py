from pydantic import BaseModel


class ContactModel(BaseModel):
    firstName: str
    lastName: str
    jobTitle: str
    email: str
    isDecisionMaker: bool

    class Config:
        extra = "allow"


class DealRequest(BaseModel):
    reference: str 
    title: str
    clientName: str
    country: str
    city: str
    ownerName: str
    ownerEmail: str
    status: str
    estimatedRevenue: float
    estimatedMargin: float
    currency: str
    contacts: list[ContactModel]

    
    class Config:
        extra = "allow"
