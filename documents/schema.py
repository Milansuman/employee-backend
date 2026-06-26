from pydantic import BaseModel, ConfigDict


class UploadDocument(BaseModel):
    filename: str
    contents: str
    mime: str


class GetAllDocumentsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    filename: str
    mime: str
