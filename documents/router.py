from fastapi import APIRouter, Depends, UploadFile
from chromadb.api.models.AsyncCollection import AsyncCollection
from sqlalchemy.ext.asyncio import AsyncSession
from db.vector_connection import get_vector_db
from db.connection import get_db
from auth.dependencies import verify_access_token, require_roles, get_current_user

from models.employee import Employee, EmployeeRoles
from documents import service, schema

document_router = APIRouter(
    prefix="/document",
    tags=["Document"],
    dependencies=[
        Depends(verify_access_token),
        Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN])),
    ],
)


@document_router.get("/", response_model=list[schema.GetAllDocumentsResponse])
async def get_all_documents(
    current_user: Employee = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_documents(employee_id=current_user.id, db=db)


@document_router.get("/{id}")
async def get_document_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    vec_db: AsyncCollection = Depends(get_vector_db),
):
    return "Not implemented"


@document_router.post("/")
async def upload_document(
    document: UploadFile,
    current_user: Employee = Depends(get_current_user),
    vec_db: AsyncCollection = Depends(get_vector_db),
    db: AsyncSession = Depends(get_db),
):
    contents = await document.read()

    if document.filename is None or document.content_type is None:
        return {"error": "something wong"}

    await service.add_document(
        employee_id=current_user.id,
        filename=document.filename,
        mime=document.content_type,
        content=contents,
        db=db,
        vec_db=vec_db,
    )
