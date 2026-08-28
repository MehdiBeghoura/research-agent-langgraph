from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel
from tavily import TavilyClient

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-20b")

class SubtopicsOutput(BaseModel):
    subtopics: list[str]
    
class VerifyOutput(BaseModel):
    is_good_enough: bool
    
class ConflictOutput(BaseModel):
    has_conflict: bool
    explanation: str | None = None
    
class ConflictResolutionOutput(BaseModel):
    conflicting_claims: list[str]
    resolution: str
    
structured_model = model.with_structured_output(SubtopicsOutput, method="json_schema")

verify_model = model.with_structured_output(VerifyOutput, method="json_schema")

conflict_model = model.with_structured_output(ConflictOutput, method="json_schema")

conflict_resolution_model = model.with_structured_output(ConflictResolutionOutput, method="json_schema")

draft_model = model

client = TavilyClient()