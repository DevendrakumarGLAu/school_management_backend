from pydantic import BaseModel

class GSTRequest(BaseModel):
    formData: str 

class GSTResponse(BaseModel):
    message: str