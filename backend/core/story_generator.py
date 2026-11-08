import os
import re
from sqlalchemy.orm import Session
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNodes
from core.models import StoryLLMResponse, StoryNodeLLM

load_dotenv()

class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        account_id = str(settings.CLOUDFLARE_ACCOUNT_ID).strip().strip('"').strip("'")
        api_token = str(settings.CLOUDFLARE_API_TOKEN).strip().strip('"').strip("'")

        return ChatOpenAI(
            model="@cf/meta/llama-3.3-70b-instruct-fp8-fast",
            base_url=f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
            api_key=api_token,
            max_tokens=2048,
        )

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object = StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            ("system", STORY_PROMPT),
            ("human", f"Create the story with this theme: {theme}")
        ])

        raw_response = llm.invoke(prompt.invoke({})) #invoke the llm with the particular prompt

        response_text = ""
        if hasattr(raw_response, 'content'):
            response_text = raw_response.content
        elif isinstance(raw_response, str):
            response_text = raw_response

        if not response_text or response_text.strip() == "null":
            raise ValueError("The LLM returned an empty response. Ensure the model has sufficient quota and is responsive.")

        if "```" in response_text:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response_text)
            if match:
                response_text = match.group(1).strip()

        response_text = re.sub(r'("\s*)\n\s*("isEnding")', r'\1,\n\2', response_text)
        response_text = re.sub(r'("\s*)\n\s*("isWinningEnding")', r'\1,\n\2', response_text)

        story_structure = story_parser.parse(response_text)
        
        story_db = Story(title=story_structure.title, session_id = session_id)
        db.add(story_db)
        db.flush() #update the story_db object with the id and stuff

        root_node_data = story_structure.rootNode #get the root node from StoryLLMResponse
 
        if isinstance(root_node_data, dict): #if its a dictionary, should validate its in a correct format
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True )

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNodes:
        node = StoryNodes(
            story_id = story_id,
            content= node_data.content if hasattr(node_data, "content") else node_data["content"], #safety check if node+data content is processed correctly
            is_root = is_root,
            is_ending= node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending= node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options = []
        )

        db.add(node)
        db.flush() 

        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            option_list = []
            for option_data  in node_data.options:
                next_node = option_data.nextNode
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                option_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })
            node.options = option_list

        db.flush()
        return node