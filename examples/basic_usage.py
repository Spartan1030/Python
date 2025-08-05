#!/usr/bin/env python3
"""
Basic usage example for GE HealthCare Intelligent Data Store SDK.

This example demonstrates:
1. Initializing the IDS client
2. Creating collections
3. Uploading documents
4. Performing semantic search
5. Running RAG queries
6. Managing prompt templates
"""

import os
import sys
from pathlib import Path

# Add the SDK to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gehc_ids import IDSClient
from gehc_ids.exceptions import IDSException


def main():
    """Main example function."""
    
    # Initialize client with credentials
    # In production, use environment variables or secure credential storage
    client = IDSClient(
        client_id="your-client-id",
        client_secret="your-client-secret",
        audience="your-audience-id"
    )
    
    # Alternative: Initialize from environment variables
    # client = IDSClient.from_environment()
    
    try:
        # 1. Health check
        print("🔍 Checking service health...")
        health = client.health_check()
        for service, status in health.items():
            print(f"  {service}: {status['status']} - {status['message']}")
        
        # 2. Vector Store Operations
        print("\n📚 Vector Store Operations")
        print("-" * 40)
        
        # Create a collection
        print("Creating collection...")
        collection = client.vector_store.create_collection(
            title="Medical Documents",
            description="Collection of medical research papers and clinical notes"
        )
        print(f"Created collection: {collection.id}")
        
        # List collections
        print("\nListing collections...")
        collections = client.vector_store.list_collections()
        for coll in collections:
            print(f"  - {coll.title} ({coll.id})")
        
        # Upload documents (example file paths)
        print("\nUploading documents...")
        file_paths = [
            "/path/to/document1.pdf",
            "/path/to/document2.txt",
            "/path/to/document3.docx"
        ]
        
        # Note: In a real scenario, ensure these files exist
        if all(os.path.exists(path) for path in file_paths):
            batch = client.vector_store.upload_documents(
                collection_id=collection.id,
                file_paths=file_paths,
                batch_name="Initial Document Upload",
                batch_description="Uploading medical research papers",
                wait_for_completion=True
            )
            print(f"Upload completed. Batch ID: {batch.id}")
        else:
            print("Skipping file upload (example files don't exist)")
            
            # Alternative: Add text chunks directly
            print("Adding text chunks instead...")
            client.vector_store.add_chunks_to_collection(
                collection_id=collection.id,
                document_id="sample-doc-1",
                document_name="Sample Medical Document",
                chunks=[
                    "Diabetes mellitus is a group of metabolic disorders characterized by high blood sugar.",
                    "Type 1 diabetes is caused by the body's inability to produce insulin.",
                    "Type 2 diabetes is characterized by insulin resistance and relative insulin deficiency."
                ],
                metadata={"source": "medical_textbook", "chapter": "endocrinology"}
            )
        
        # Semantic search
        print("\nPerforming semantic search...")
        search_results = client.vector_store.semantic_search(
            collection_id=collection.id,
            query="What are the main types of diabetes?",
            limit=5
        )
        
        print(f"Found {len(search_results)} relevant documents:")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. Score: {result.score:.3f}")
            print(f"     Content: {result.content[:100]}...")
        
        # RAG query
        print("\nPerforming RAG query...")
        rag_response = client.vector_store.rag_query(
            collection_id=collection.id,
            message="Explain the different types of diabetes and their characteristics",
            limit=3
        )
        
        print("RAG Response:")
        print(f"Answer: {rag_response.answer}")
        print(f"Sources used: {len(rag_response.sources)}")
        
        # 3. Prompt Store Operations
        print("\n📝 Prompt Store Operations")
        print("-" * 40)
        
        # Create a prompt template
        print("Creating prompt template...")
        prompt = client.prompt_store.create_prompt_template(
            name="Medical_Summary_Prompt",
            content="Based on the following medical context: {context}\n\nPlease provide a concise summary for the question: {question}",
            type="System",
            provider="OpenAI",
            params='{"model": "gpt-3.5-turbo", "temperature": 0.7, "max_tokens": 200}',
            category="summarization",
            tags=["medical", "summary", "clinical"]
        )
        print(f"Created prompt: {prompt.name} (version {prompt.version})")
        
        # Create a new version
        print("\nCreating new prompt version...")
        updated_prompt = client.prompt_store.create_prompt_version(
            name="Medical_Summary_Prompt",
            content="You are a medical AI assistant. Using the medical context provided: {context}\n\nProvide a detailed and accurate answer to: {question}",
            params='{"model": "gpt-4", "temperature": 0.5, "max_tokens": 300}',
            tags=["medical", "detailed", "clinical", "gpt4"]
        )
        print(f"Created version {updated_prompt.version}")
        
        # Set as default
        print("Setting new version as default...")
        client.prompt_store.set_default_version(
            name="Medical_Summary_Prompt",
            version=updated_prompt.version,
            justification="Upgraded to GPT-4 for better medical accuracy"
        )
        
        # List all prompts
        print("\nListing prompt templates...")
        prompt_list = client.prompt_store.get_all_prompts()
        print(f"Total prompts: {prompt_list.total_count}")
        for p in prompt_list.prompts:
            default_marker = " (DEFAULT)" if p.default else ""
            print(f"  - {p.name} v{p.version}{default_marker}")
        
        # Get default prompt
        print("\nRetrieving default prompt...")
        default_prompt = client.prompt_store.get_default_prompt("Medical_Summary_Prompt")
        print(f"Default version: {default_prompt.version}")
        print(f"Content preview: {default_prompt.content[:50]}...")
        
        # 4. Advanced RAG with Custom Prompt
        print("\n🚀 Advanced RAG with Custom Prompt")
        print("-" * 40)
        
        # This would typically integrate the prompt with the RAG query
        # Note: The actual integration depends on LMaaS service configuration
        rag_with_prompt = client.vector_store.rag_query(
            collection_id=collection.id,
            message="What are the symptoms of Type 1 diabetes?",
            limit=3
        )
        
        print("Advanced RAG Response:")
        print(f"Answer: {rag_with_prompt.answer}")
        
        # 5. Cleanup (optional)
        print("\n🧹 Cleanup")
        print("-" * 40)
        
        # Count records
        record_count = client.vector_store.count_records(collection.id)
        print(f"Records in collection: {record_count.count}")
        
        # List documents
        documents = client.vector_store.list_documents(collection.id)
        print(f"Documents in collection: {len(documents.documents)}")
        
        # Uncomment to delete the collection
        # print("Deleting collection...")
        # client.vector_store.delete_collection(collection.id, soft_delete=True)
        # print("Collection deleted (soft delete)")
        
        print("\n✅ Example completed successfully!")
        
    except IDSException as e:
        print(f"\n❌ IDS SDK Error: {e.message}")
        print(f"Status Code: {e.status_code}")
        if e.response_data:
            print(f"Response Data: {e.response_data}")
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()