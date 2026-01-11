import os
from mem0 import AsyncMemory
from mem0.configs.base import MemoryConfig, EmbedderConfig, VectorStoreConfig, LlmConfig

from langchain.tools import tool
from loguru import logger
import asyncio

from src.slack_integrations_online.config import settings

# ------------------------------------------------------------------
# ENV
# ------------------------------------------------------------------
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# ------------------------------------------------------------------
# MEM0 CONFIG with error handling
# ------------------------------------------------------------------
memory = {}
try:
    memory_config = MemoryConfig(
        embedder=EmbedderConfig(
            provider="openai",
            config={"model": "text-embedding-3-small"},
        ),
        llm=LlmConfig(
            provider="openai",
            config={"model": "gpt-4o-mini", "temperature": 0.0},
        ),
        vector_store=VectorStoreConfig(
            provider="mongodb",
            config={
                "db_name": settings.MONGODB_DATABASE_NAME,
                "collection_name": "memory",
                "mongo_uri": settings.MONGODB_URI,
                "embedding_model_dims": 1536
            },
        ),
    )
    
    memory = AsyncMemory(config=memory_config)
    logger.info("Memory system initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize memory system: {str(e)}")
    logger.info("ℹContinuing without memory functionality")

# ------------------------------------------------------------------
# SYNC TOOLS (for LangGraph)
# ------------------------------------------------------------------

@tool
def search_memory(query: str) -> str:
    """
    Search conversational memory.
    Returns 'No previous conversations found.' if nothing is found.
    """
    try:
        if memory is None:
            logger.info("ℹ Memory system not available")
            return "Memory system not available."
        
        # Run async function in sync context
        return asyncio.run(_search_memory_async(query, "default_user"))
    except Exception as e:
        logger.error(f"Memory search failed: {str(e)}")
        return "No previous conversations found."


async def _search_memory_async(query: str, user_id: str = "default_user") -> str:
    """Async implementation."""
    try:
        if memory is None:
            return "Memory system not available."
            
        logger.info(f"Searching memory for user: {user_id}")
        results = await memory.search(
            query=query,
            user_id=user_id,
            limit=3,
        )

        if not results or not results.get("results"):
            logger.info(f"ℹNo previous memories found for user: {user_id}")
            return "No previous conversations found."

        memories = "\n".join(
            f"- {r['memory']}" for r in results["results"]
        )

        logger.info(f"Retrieved {len(results['results'])} memories")
        return f"Previous conversations:\n{memories}"
    except Exception as e:
        logger.error(f"Memory search failed: {str(e)}")
        return "No previous conversations found."


@tool
def add_to_memory(content: str) -> str:
    """
    Store content into long-term memory.
    """
    try:
        if memory is None:
            logger.info("ℹMemory system not available")
            return "Memory system not available."
            
        # Run async function in sync context
        return asyncio.run(_add_to_memory_async(content, "default_user"))
    except Exception as e:
        logger.error(f"Failed to store memory: {str(e)}")
        return f"Error storing memory: {str(e)}"


async def _add_to_memory_async(content: str, user_id: str = "default_user") -> str:
    """Async implementation."""
    try:
        if memory is None:
            return "Memory system not available."
            
        logger.info(f" Storing memory for user: {user_id}")
        await memory.add(
            [{"role": "user", "content": content}],
            user_id=user_id,
        )

        logger.info(" Memory stored successfully")
        return "Memory stored successfully."
    except Exception as e:
        logger.error(f"Failed to store memory: {str(e)}")
        return f"Error storing memory: {str(e)}"