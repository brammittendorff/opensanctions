from datetime import datetime
from typing import Dict, List, TypedDict, Union
from pydantic import BaseModel, Field


class EntityResponse(BaseModel):
    id: str
    schema_: str = Field("LegalEntity", alias="schema")
    properties: Dict[str, List[Union[str, "EntityResponse"]]]
    datasets: List[str]
    referents: List[str]
    first_seen: datetime
    last_seen: datetime


EntityResponse.update_forward_refs()


class SearchResponse(BaseModel):
    results: List[EntityResponse]


class FreebaseType(TypedDict):
    id: str
    name: str