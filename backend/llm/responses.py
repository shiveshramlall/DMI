"""
D&D Assistant Response Models and LLM Integration

This module provides Pydantic models and an assistant class for handling D&D-related
queries using various LLM backends (llama.cpp or Ollama). It structures responses
for NPCs, locations, items, and other D&D game elements.

Classes:
    Answer: Model for general query responses
    NPC: Model for Non-Player Character details
    Location: Model for location descriptions
    Puzzle: Model for game puzzles
    Item: Model for game items
    Rumour: Model for in-game rumors
    GeneratedName: Model for fantasy name generation

    InstructorAssistant: Main class for handling LLM interactions
"""

from pydantic import BaseModel, Field
from typing import List, Type, TypeVar
import instructor
import llama_cpp
from llama_cpp.llama_speculative import LlamaPromptLookupDecoding

T = TypeVar("T", bound=BaseModel)

# --- List of all response models ---


class Answer(BaseModel):
    answer: str = Field(..., description="Exact requirement as per the user's query.")
    references: List[str] = Field(
        ...,
        description="Key points or facts pulled from the documents. Include Metadata if available.",
    )


class NPC(BaseModel):
    name: str = Field(
        ...,
        description="The full name and surname of the Non-Player Character. Fantasy themed.",
    )
    race: str = Field(
        ..., description="Dungeons and Dragons race, e.g. 'human', 'elf', 'dwarf'."
    )
    role: str = Field(
        ...,
        description="The NPC's role or profession, e.g. 'blacksmith' or 'village elder'.",
    )
    description: str = Field(
        ...,
        description="A brief summary of the NPC's personality, appearance, and mannerisms.",
    )
    motivation: str = Field(..., description="What the NPC wants or cares about.")
    secret: str = Field(..., description="A hidden detail or twist about the NPC.")


class Location(BaseModel):
    name: str = Field(..., description="The name of the location.")
    type: str = Field(
        ..., description="Type of location, e.g. 'village', 'ruin', 'forest'."
    )
    description: str = Field(
        ..., description="A vivid description of the place and its key features."
    )
    danger_level: int = Field(
        ...,
        description="An integer from 1 (safe) to 10 (deadly), indicating how dangerous this place is.",
    )
    rumors: List[str] = Field(
        ..., description="Rumors or local stories associated with the location."
    )


class Puzzle(BaseModel):
    title: str = Field(..., description="The name or short title of the puzzle.")
    description: str = Field(
        ...,
        description="A full description of the puzzle setup and how it is presented to players.",
    )
    solution: str = Field(..., description="The correct solution to the puzzle.")
    hints: List[str] = Field(
        ...,
        description="Clues or hints that can be revealed to help players solve the puzzle.",
    )


class Item(BaseModel):
    name: str = Field(..., description="The name of the magical or mundane item.")
    item_type: str = Field(
        ..., description="The type of item, e.g. 'weapon', 'armor', 'trinket'."
    )
    rarity: str = Field(
        ...,
        description="The rarity of the item: Common, Uncommon, Rare, Very Rare, or Legendary.",
    )
    description: str = Field(
        ..., description="A description of the item's appearance and properties."
    )
    effect: str = Field(
        ..., description="The mechanical or magical effect of the item."
    )


class Rumour(BaseModel):
    text: str = Field(..., description="The content of the rumor.")
    truthfulness: str = Field(
        ..., description="Whether the rumor is True, False, or Half-True."
    )
    source: str = Field(..., description="Who or where the rumor originated from.")


class GeneratedName(BaseModel):
    name: str = Field(..., description="The generated name.")
    culture: str = Field(
        ...,
        description="The cultural or fantasy context the name belongs to, e.g. 'Elvish', 'Dwarvish', 'Pirate'.",
    )
    meaning: str = Field(
        ..., description="A symbolic or linguistic meaning for the name, if applicable."
    )


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


# --- Instructor Assistant Class ---
# This class handles the interaction with the LLM backend, either Ollama or llama.cpp.


class InstructorAssistant:
    """
    A D&D-focused assistant that interfaces with different LLM backends.

    This class provides a unified interface for querying language models
    about D&D-related content (markdown files embedded and then stored in ChromaDB),
    supporting both local models via llama.cpp
    and remote models via Ollama.

    Attributes:
        model (str): Identifier for the LLM model being used
        create: Function for creating chat completions (varies by backend)
    """

    def __init__(
        self,
        model: str,
    ):
        """
        Initialize the assistant with specified model backend.

        Supports both local llama.cpp models (for customization)
        and local Ollama models.

        Args:
            model (str): Model identifier. Use "custom" for local llama.cpp model,
                        or model name for Ollama (e.g., "mistral")
        """

        if model.lower() == "custom":
            print("Using custom model with llama_cpp")
            llama = llama_cpp.Llama(
                model_path=r"C:\Users\shive\.lmstudio\models\lmstudio-community\Mistral-7B-Instruct-v0.3-GGUF\Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
                n_gpu_layers=-1,
                chat_format="chatml",
                n_batch=512,
                n_ctx=8192,
                draft_model=LlamaPromptLookupDecoding(num_pred_tokens=2),
                logits_all=True,
                verbose=False,
                low_vram=True,
                f16_kv=True,
            )

            self.create = instructor.patch(
                create=llama.create_chat_completion_openai_v1,
                mode=instructor.Mode.JSON_SCHEMA,
            )

        else:

            print(f"Using instructor model from ollama: {model}")
            client = instructor.from_provider(
                "ollama/" + model,
                mode=instructor.Mode.JSON,
            )

            self.create = client.chat.completions.create

        self.model = model

    def build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Construct a prompt for the LLM combining query and context.

        Args:
            query (str): User's question or request
            context (str): Additional context or relevant documents

        Returns:
            str: Formatted prompt string
        """

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
        """
        Send a query to the LLM and get a structured response.

        Args:
            query (str): The user's question or request
            context (str): Additional context or relevant documents
            response_model (Type[T]): Pydantic model class for response structure

        Returns:
            T: Instance of response_model containing the structured response

        Raises:
            instructor.exceptions.ValidationError: If response doesn't match model
        """

        prompt = self.build_prompt(query, context)

        response = self.create(
            messages=[{"role": "user", "content": prompt}],
            response_model=response_model,
            max_retries=5,
        )

        return response
