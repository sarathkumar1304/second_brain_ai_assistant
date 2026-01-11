from langchain.tools import tool
from loguru import logger
import asyncio

from src.slack_integrations_online.application.rag.retrievers import get_retriever
from src.slack_integrations_online.application.rag.single_document_retriever import (
    get_single_document,
)


# ---------------------------------------------------------
# SYNC TOOLS (for LangGraph)
# ---------------------------------------------------------

@tool
def mongodb_retriever_tool(query: str) -> str:
    """
    Retrieve relevant documents from MongoDB using vector search.
    Returns '__NO_CONTEXT__' if no relevant documents are found.
    """
    logger.info(f"mongodb_retriever_tool called with query: '{query}'")
    try:
        # Run async function in sync context
        result = asyncio.run(_mongodb_retriever_tool_async(query))
        logger.info(f"mongodb_retriever_tool returned {len(result)} characters")
        return result
    except Exception as e:
        logger.error(f"MongoDB retriever tool failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return "__NO_CONTEXT__"


async def _mongodb_retriever_tool_async(query: str) -> str:
    """Async implementation."""
    logger.info(f"Starting MongoDB search for: '{query}'")
    try:
        retriever = get_retriever(
            embedding_model_id="text-embedding-3-small",
            k=3,
        )
        logger.info(f"Retriever created successfully")

        # Run the synchronous invoke in a thread pool
        loop = asyncio.get_event_loop()
        logger.info(f"Invoking retriever...")
        docs = await loop.run_in_executor(None, retriever.invoke, query)
        logger.info(f"Retriever returned {len(docs)} documents")

        if not docs:
            logger.warning("MongoDB retriever returned 0 documents")
            return "__NO_CONTEXT__"

        formatted_docs = []

        for i, doc in enumerate(docs, start=1):
            title = doc.metadata.get("title", "Untitled")
            url = doc.metadata.get("url", "UNKNOWN_URL")
            content = doc.page_content.strip()
            
            logger.info(f"Document {i}: {title} | URL: {url} | Content: {len(content)} chars")

            formatted_docs.append(
                f"""
<document id="{i}">
<title>{title}</title>
<url>{url}</url>
<content>
{content}
</content>
</document>
""".strip()
            )

        result = "\n".join(formatted_docs)
        final_output = f"""
<search_results>
{result}
</search_results>

INSTRUCTIONS:
- Use ONLY the content above to answer
- Always cite the document URL when using information
""".strip()
        
        logger.info(f"MongoDB search completed successfully")
        return final_output

    except Exception as e:
        logger.exception(f" MongoDB retriever tool failed: {str(e)}")
        return "__NO_CONTEXT__"


@tool
def get_complete_docs_with_url(url: str) -> str:
    """
    Fetch the complete raw document using its URL.
    """
    logger.info(f" get_complete_docs_with_url called with URL: '{url}'")
    try:
        # Run async function in sync context
        result = asyncio.run(_get_complete_docs_with_url_async(url))
        return result
    except Exception as e:
        logger.error(f" Failed to fetch full document: {str(e)}")
        return "__NO_CONTEXT__"


async def _get_complete_docs_with_url_async(url: str) -> str:
    """Async implementation."""
    try:
        # Run the synchronous function in a thread pool
        loop = asyncio.get_event_loop()
        document = await loop.run_in_executor(None, get_single_document, url)

        if not document or "<error>" in document:
            logger.warning(f" No document found for URL: {url}")
            return "__NO_CONTEXT__"

        logger.info(f" Retrieved full document for URL: {url}")
        return document

    except Exception as e:
        logger.exception(f" Failed to fetch full document: {str(e)}")
        return "__NO_CONTEXT__"