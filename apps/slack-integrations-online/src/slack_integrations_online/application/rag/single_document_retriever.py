from pymongo import MongoClient

from src.slack_integrations_online.config import settings


def get_single_document(url: str) -> str:
    """Retrieve a single document from MongoDB by URL and format as XML.
    
    Args:
        url: URL of the document to retrieve from the database.
    
    Returns:
        str: XML-formatted document with URL and content.
    """

    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DATABASE_NAME]
        
        # Try raw collection first
        collection = db['raw']
        document = collection.find_one({"metadata.url": url})
        
        # If not found in raw, try rag collection
        if not document:
            collection = db['rag']
            document = collection.find_one({"url": url})
        
        if not document:
            return f"<error>No document found with URL: {url}</error>"

        # Extract content from appropriate field
        if 'content' in document:
            content = document.get('content', '')
        elif 'chunk' in document:
            content = document.get('chunk', '')
        else:
            content = ''
        
        # Get URL
        doc_url = document.get('url', url)
        if not doc_url and 'metadata' in document:
            doc_url = document.get('metadata', {}).get('url', url)

        # Format the result in XML structure
        result = f"""
        <document>
        <url>{doc_url}</url>
        <content>{content.strip()}</content>
        </document>
        """

        return result

    except Exception as e:
        return f"<error>Error retrieving document: {str(e)}</error>"
    
    finally:
        if 'client' in locals():
            client.close()