from langchain.agents import create_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from support_agent.llm import llm
from support_agent.prompt import SYSTEM_PROMPT
from support_agent.tool import (
    # get_all_departments,
    # get_all_employees,
    # get_department_by_id,
    # get_employee_by_id,
    query_documents,
)

from support_agent.schema import RuntimeContext


def get_agent(checkpointer: AsyncPostgresSaver):
    agent = create_agent(
        model=llm,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            # get_all_departments,
            # get_all_employees,
            # get_department_by_id,
            # get_employee_by_id,
            query_documents
        ],
        checkpointer=checkpointer,
        context_schema=RuntimeContext,
    )

    return agent
