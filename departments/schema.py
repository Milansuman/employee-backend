from pydantic import BaseModel, ConfigDict, Field

class CreateOrUpdateDepartment(BaseModel):
    name: str = Field(min_length=1)

class DepartmentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
