from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel): #description is for the llms
    text: str = Field(description="the text of the option shown to the user")
    nextNode: Dict[str, Any] = Field(description="the next node content and its content")


class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story")
    isEnding: bool = Field(default=False, description="Whether this node is an ending nodes")
    isWinningEnding: bool = Field(default=False, description="Whether this node is a winning ending nodes")
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="The option for the node")

class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story")