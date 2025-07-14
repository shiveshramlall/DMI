from openai import OpenAI
from pydantic import BaseModel, Field, RootModel
from typing import List, Type, TypeVar
import instructor

T = TypeVar("T", bound=BaseModel)

class Answer(BaseModel):
    answer: str = Field(..., description="Exact requirement as per the user's query.")
    references: List[str] = Field(..., description="Key points or facts pulled from the documents. Include Metadata if available.")

class NPC(BaseModel):
    name: str = Field(..., description="The full name and surname of the Non-Player Character. Fantasy themed.")
    race: str = Field(..., description="Dungeons and Dragons race, e.g. 'human', 'elf', 'dwarf'.")
    role: str = Field(..., description="The NPC's role or profession, e.g. 'blacksmith' or 'village elder'.")
    description: str = Field(..., description="A brief summary of the NPC's personality, appearance, and mannerisms.")
    motivation: str = Field(..., description="What the NPC wants or cares about.")
    secret: str = Field(..., description="A hidden detail or twist about the NPC.")

class Location(BaseModel):
    name: str = Field(..., description="The name of the location.")
    type: str = Field(..., description="Type of location, e.g. 'village', 'ruin', 'forest'.")
    description: str = Field(..., description="A vivid description of the place and its key features.")
    danger_level: int = Field(..., description="An integer from 1 (safe) to 10 (deadly), indicating how dangerous this place is.")
    rumors: List[str] = Field(..., description="Rumors or local stories associated with the location.")

class Puzzle(BaseModel):
    title: str = Field(..., description="The name or short title of the puzzle.")
    description: str = Field(..., description="A full description of the puzzle setup and how it is presented to players.")
    solution: str = Field(..., description="The correct solution to the puzzle.")
    hints: List[str] = Field(..., description="Clues or hints that can be revealed to help players solve the puzzle.")

class Item(BaseModel):
    name: str = Field(..., description="The name of the magical or mundane item.")
    item_type: str = Field(..., description="The type of item, e.g. 'weapon', 'armor', 'trinket'.")
    rarity: str = Field(..., description="The rarity of the item: Common, Uncommon, Rare, Very Rare, or Legendary.")
    description: str = Field(..., description="A description of the item's appearance and properties.")
    effect: str = Field(..., description="The mechanical or magical effect of the item.")

class Rumour(BaseModel):
    text: str = Field(..., description="The content of the rumor.")
    truthfulness: str = Field(..., description="Whether the rumor is True, False, or Half-True.")
    source: str = Field(..., description="Who or where the rumor originated from.")

class GeneratedName(BaseModel):
    name: str = Field(..., description="The generated name.")
    culture: str = Field(..., description="The cultural or fantasy context the name belongs to, e.g. 'Elvish', 'Dwarvish', 'Pirate'.")
    meaning: str = Field(..., description="A symbolic or linguistic meaning for the name, if applicable.")

class NPCList(BaseModel):
    NPCs: List[NPC]

class LocationList(BaseModel):
    locations: List[Location]

class PuzzleList(BaseModel):
    puzzles: List[Puzzle]

class ItemList(BaseModel):
    items: List[Item]

class RumourList(BaseModel):
    rumours: List[Rumour]  

class GeneratedNameList(BaseModel):
    names: List[GeneratedName]

class InstructorAssistant:

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
    ):
        openai_client = OpenAI(base_url=base_url, api_key=api_key)
        self.client = instructor.from_openai(openai_client, mode=instructor.Mode.JSON)
        self.model = model

    def build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        return f"""
        ==================
        You are a virtual assistant for a Dungeon Master running Dungeons & Dragons (D&D) sessions.

        - Helping prepare and run sessions by providing ideas, rules clarifications, encounter design, and narrative suggestions.
        - Answering queries using provided campaign documents, focusing only on the relevant content.
        - If no documents are provided, rely on your general D&D knowledge (primarily 5th Edition unless specified).

        Be accurate, concise, and helpful. Prioritize clarity when referencing documents. Prioritize clarity and creativity when assisting with gameplay and storytelling.
        ==================

        ==================
        DOCUMENT CONTEXT:
        {context}
        ==================

        ==================
        Query:
        {query}
        ==================
        """

    def ask(
        self,
        query: str,
        context: str,
        response_model: Type[T],
    ):
        prompt = self.build_prompt(query, context)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_model=response_model,
        )
        return response
