#define python classes with a specific type of data that the api should accept or return

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

#pydantic makes it so that we don't need to check the data is correctly structued, and instead is done automatically by pydantic

class StoryOptionsSchema(BaseModel):
    text: str
    node_id: Optional[int] = None

class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False

#what the response from the api should be
class CompleteStoryNodeResponse(StoryNodeBase): #inherit from StoryNodeBase
    id: int
    options: List[StoryOptionsSchema] = []

    class Config:
        from_attributes = True


class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = True

    class Config:
        from_attributes = True

class CreateStoryRequest(BaseModel):
    theme: str

class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        from_attributes = True