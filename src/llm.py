from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-20b")


class SubtopicsOutput(BaseModel):
    subtopics: list[str]


structured_model = model.with_structured_output(SubtopicsOutput)