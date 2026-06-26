from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from env import env

llm = ChatOpenAI(
    base_url=env.OPENAI_BASE_URL,
    api_key=SecretStr(env.OPENAI_API_KEY),
    model="openai/gpt-oss-20b",
)
