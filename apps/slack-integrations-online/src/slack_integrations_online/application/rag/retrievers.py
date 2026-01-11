from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.retrievers.hybrid_search import MongoDBAtlasHybridSearchRetriever
from loguru import logger

from src.slack_integrations_online.application.rag.embeddings import get_openai_embedding_model
from src.slack_integrations_online.config import settings


def get_retriever(
    embedding_model_id: str, k: int = 3
) -> MongoDBAtlasHybridSearchRetriever:
    """Create a MongoDB Atlas hybrid search retriever with specified embedding model."""
    
    try:
        embedding_model = get_openai_embedding_model(model_id=embedding_model_id)
        logger.info(f"Using embedding model: {embedding_model_id}")
        
        return get_hybrid_search_retriever(embedding_model=embedding_model, k=k)
    except Exception as e:
        logger.error(f"Failed to create retriever: {str(e)}")
        raise


def get_hybrid_search_retriever(
    embedding_model: OpenAIEmbeddings, k: int = 3
) -> MongoDBAtlasHybridSearchRetriever:
    """Create a MongoDB Atlas hybrid search retriever."""
    
    try:
        logger.info(f"Creating vector store for namespace: {settings.MONGODB_DATABASE_NAME}.rag")
        
        vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
            connection_string=settings.MONGODB_URI,
            embedding=embedding_model,
            namespace=f"{settings.MONGODB_DATABASE_NAME}.rag",
            text_key="chunk",
            embedding_key="embedding",
            relevance_score_fn="dotProduct"
        )
        
        logger.info(f"Creating retriever with index: chunk_text_search, k={k}")
        
        retriever = MongoDBAtlasHybridSearchRetriever(
            vectorstore=vectorstore,
            search_index_name="chunk_text_search",
            top_k=k,
            vector_penalty=0,  # Changed from 50 to 0
            fulltext_penalty=0  # Changed from 50 to 0
        )
        
        return retriever
        
    except Exception as e:
        logger.error(f"Failed to create hybrid search retriever: {str(e)}")
        raise