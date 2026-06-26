from langchain.tools import ToolRuntime, tool
from documents import service as doc_service
from support_agent.schema import RuntimeContext

# @tool
# async def get_all_employees():
#     pass

# @tool
# async def get_employee_by_id():
#     pass

# @tool
# async def get_all_departments():
#     pass

# @tool
# async def get_department_by_id():
#     pass


@tool
async def query_documents(
    query: str, top_k: int, runtime: ToolRuntime[RuntimeContext]
) -> str:
    """
    A tool to query policy documents
    """
    chunks = await doc_service.query_documents(
        query=query, top_k=top_k, vec_db=runtime.context.vec_db
    )

    return "\n".join(chunks)
