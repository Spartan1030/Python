#!/usr/bin/env python3
"""
Vector Store focused example for GE HealthCare IDS SDK.

This example demonstrates a complete document management workflow:
1. Creating and managing collections
2. Bulk document upload with status monitoring
3. Adding custom text chunks
4. Semantic search with metadata filtering
5. RAG queries for document-based Q&A
6. Document and collection management
"""

import os
import time
from pathlib import Path

from gehc_ids import VectorStoreClient, IDSAuth
from gehc_ids.exceptions import IDSException


def create_sample_documents(temp_dir: Path) -> list:
    """Create sample documents for testing."""
    documents = []
    
    # Sample medical documents
    sample_content = [
        {
            "filename": "diabetes_overview.txt",
            "content": """
Diabetes Mellitus: A Comprehensive Overview

Diabetes mellitus is a group of metabolic disorders characterized by high blood sugar (glucose) levels over a prolonged period. There are primarily three main types of diabetes:

Type 1 Diabetes:
- Also known as insulin-dependent diabetes or juvenile diabetes
- Usually develops in children, teenagers, and young adults
- The body's immune system attacks and destroys the insulin-producing beta cells of the pancreas
- Requires daily insulin injections for survival
- Accounts for 5-10% of all diabetes cases

Type 2 Diabetes:
- The most common form of diabetes, accounting for 90-95% of cases
- Usually develops in adults over 45, but increasingly seen in younger people
- The body becomes resistant to insulin or doesn't produce enough insulin
- Can often be managed with lifestyle changes and oral medications
- Risk factors include obesity, sedentary lifestyle, and genetics

Gestational Diabetes:
- Develops during pregnancy
- Usually resolves after delivery but increases risk of Type 2 diabetes later
- Requires careful monitoring and management during pregnancy

Symptoms include frequent urination, excessive thirst, unexplained weight loss, fatigue, and blurred vision.
            """
        },
        {
            "filename": "cardiovascular_disease.txt", 
            "content": """
Cardiovascular Disease: Understanding Heart Health

Cardiovascular disease (CVD) refers to conditions that involve narrowed or blocked blood vessels that can lead to a heart attack, chest pain (angina) or stroke. Other heart conditions, such as those that affect your heart's muscle, valves or rhythm, also are considered forms of heart disease.

Common Types:
1. Coronary Artery Disease (CAD)
   - Most common type of heart disease
   - Caused by plaque buildup in arteries
   - Can lead to heart attacks

2. Heart Failure
   - Heart can't pump blood efficiently
   - Can be caused by CAD, high blood pressure, or diabetes
   - Symptoms include shortness of breath, fatigue, swelling

3. Arrhythmias
   - Irregular heartbeats
   - Can be too fast, too slow, or irregular
   - Some are harmless, others can be life-threatening

Risk Factors:
- High blood pressure
- High cholesterol
- Diabetes
- Smoking
- Obesity
- Sedentary lifestyle
- Family history

Prevention strategies include regular exercise, healthy diet, not smoking, and managing stress.
            """
        },
        {
            "filename": "mental_health_basics.txt",
            "content": """
Mental Health: Understanding Psychological Wellbeing

Mental health includes our emotional, psychological, and social well-being. It affects how we think, feel, and act. It also helps determine how we handle stress, relate to others, and make choices.

Common Mental Health Conditions:

Depression:
- Persistent feelings of sadness, hopelessness, or emptiness
- Loss of interest in activities once enjoyed
- Changes in appetite, sleep patterns, and energy levels
- Difficulty concentrating and making decisions
- Treatment includes therapy, medication, and lifestyle changes

Anxiety Disorders:
- Excessive worry or fear that interferes with daily activities
- Types include generalized anxiety, panic disorder, social anxiety
- Physical symptoms can include rapid heartbeat, sweating, trembling
- Treatment options include cognitive behavioral therapy and medications

Bipolar Disorder:
- Extreme mood swings including emotional highs (mania) and lows (depression)
- Manic episodes involve elevated mood, increased activity, and poor judgment
- Depressive episodes involve symptoms similar to major depression
- Requires ongoing treatment and mood stabilizers

Importance of Mental Health:
- Affects physical health and quality of life
- Impacts relationships and work performance
- Early intervention improves outcomes
- Reducing stigma encourages people to seek help

Support resources include therapy, support groups, medication when appropriate, and lifestyle modifications.
            """
        }
    ]
    
    # Create temporary directory and files
    temp_dir.mkdir(exist_ok=True)
    
    for doc in sample_content:
        file_path = temp_dir / doc["filename"]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])
        documents.append(str(file_path))
    
    return documents


def main():
    """Main example function."""
    
    # Initialize authentication and client
    auth = IDSAuth(
        client_id="your-client-id",
        client_secret="your-client-secret", 
        audience="your-audience-id"
    )
    
    client = VectorStoreClient(auth=auth)
    
    try:
        # 1. Health checks
        print("🔍 Checking Vector Store services...")
        
        try:
            vector_health = client.health_check_vector_db()
            print(f"Vector DB: {vector_health.status}")
        except Exception as e:
            print(f"Vector DB: Error - {e}")
        
        try:
            query_health = client.health_check_query_service()
            print(f"Query Service: {query_health.status}")
        except Exception as e:
            print(f"Query Service: Error - {e}")
        
        try:
            batch_health = client.health_check_batch_service()
            print(f"Batch Service: {batch_health.status}")
        except Exception as e:
            print(f"Batch Service: Error - {e}")
        
        # 2. Create collection
        print("\n📁 Creating medical documents collection...")
        collection = client.create_collection(
            title="Medical_Knowledge_Base",
            description="Comprehensive collection of medical documents and research papers for healthcare AI applications"
        )
        print(f"Created collection: {collection.title} (ID: {collection.id})")
        
        # 3. Document upload workflow
        print("\n📄 Document Upload Workflow")
        print("-" * 40)
        
        # Create sample documents
        temp_dir = Path("temp_medical_docs")
        try:
            file_paths = create_sample_documents(temp_dir)
            print(f"Created {len(file_paths)} sample documents")
            
            # Upload documents
            print("Starting bulk document upload...")
            batch = client.upload_documents(
                collection_id=collection.id,
                file_paths=file_paths,
                batch_name="Medical Knowledge Upload",
                batch_description="Initial upload of medical reference documents",
                wait_for_completion=True,
                poll_interval=10,
                max_wait_time=600
            )
            
            print(f"Upload completed! Batch ID: {batch.id}")
            
            # Check batch results
            if batch.files:
                successful = sum(1 for f in batch.files.values() if f.status == "success")
                failed = sum(1 for f in batch.files.values() if f.status == "failed")
                print(f"Results: {successful} successful, {failed} failed")
                
                if failed > 0:
                    print("Failed files:")
                    for file_id, file_info in batch.files.items():
                        if file_info.status == "failed":
                            print(f"  - {file_info.file_path}: {file_info.error}")
        
        finally:
            # Cleanup temporary files
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
                print("Cleaned up temporary files")
        
        # 4. Add custom text chunks
        print("\n📝 Adding custom text chunks...")
        client.add_chunks_to_collection(
            collection_id=collection.id,
            document_id="clinical-guidelines-001",
            document_name="Clinical Practice Guidelines",
            chunks=[
                "Regular blood glucose monitoring is essential for diabetes management.",
                "HbA1c levels should be checked every 3-6 months for diabetic patients.",
                "Lifestyle modifications including diet and exercise are first-line treatments for Type 2 diabetes.",
                "Insulin therapy may be required when oral medications are insufficient."
            ],
            metadata={
                "source": "clinical_guidelines",
                "specialty": "endocrinology",
                "evidence_level": "A",
                "year": "2024"
            }
        )
        print("Added clinical guideline chunks")
        
        # 5. List and explore collection contents
        print("\n📊 Collection Management")
        print("-" * 40)
        
        # Count records
        record_count = client.count_records(collection.id)
        print(f"Total records in collection: {record_count.count}")
        
        # List documents
        documents = client.list_documents(collection.id, page=1, size=10)
        print(f"Documents in collection: {len(documents.documents)}")
        for doc in documents.documents:
            print(f"  - {doc.name} (ID: {doc.id})")
        
        # List all collections
        all_collections = client.list_collections()
        print(f"\nAll collections: {len(all_collections)}")
        for coll in all_collections:
            print(f"  - {coll.title}: {coll.description}")
        
        # 6. Semantic Search Examples
        print("\n🔍 Semantic Search Examples")
        print("-" * 40)
        
        search_queries = [
            "What are the symptoms of diabetes?",
            "How is cardiovascular disease prevented?",
            "What treatments are available for depression?",
            "Blood glucose monitoring guidelines"
        ]
        
        for query in search_queries:
            print(f"\nQuery: '{query}'")
            results = client.semantic_search(
                collection_id=collection.id,
                query=query,
                limit=3
            )
            
            if results:
                print(f"Found {len(results)} relevant results:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. Relevance: {result.score:.3f}")
                    print(f"     Content: {result.content[:150]}...")
                    if result.metadata:
                        print(f"     Metadata: {result.metadata}")
            else:
                print("  No results found")
        
        # 7. RAG Query Examples
        print("\n🧠 RAG Query Examples")
        print("-" * 40)
        
        rag_questions = [
            "What are the main differences between Type 1 and Type 2 diabetes?",
            "How can someone reduce their risk of cardiovascular disease?",
            "What are the warning signs of depression that people should watch for?"
        ]
        
        for question in rag_questions:
            print(f"\nQuestion: {question}")
            print("-" * 60)
            
            rag_response = client.rag_query(
                collection_id=collection.id,
                message=question,
                limit=5
            )
            
            print(f"Answer: {rag_response.answer}")
            
            if rag_response.sources:
                print(f"\nBased on {len(rag_response.sources)} sources:")
                for i, source in enumerate(rag_response.sources, 1):
                    print(f"  {i}. {source.content[:100]}... (Score: {source.score:.3f})")
        
        # 8. Advanced search with metadata filtering
        print("\n🎯 Advanced Search with Metadata Filtering")
        print("-" * 40)
        
        # Search with metadata filter
        filtered_results = client.semantic_search(
            collection_id=collection.id,
            query="diabetes management",
            limit=5,
            metadata={"specialty": "endocrinology"}
        )
        
        print(f"Results filtered by specialty='endocrinology': {len(filtered_results)}")
        for result in filtered_results:
            print(f"  - {result.content[:100]}...")
        
        # 9. Batch status monitoring example
        print("\n⏱️ Batch Management")
        print("-" * 40)
        
        # Get all batches
        batches = client.get_batches(detailed=True, limit=5)
        print(f"Recent batches: {len(batches.get('batches', []))}")
        
        # 10. Document management
        print("\n🗑️ Document Management")
        print("-" * 40)
        
        # This would delete a specific document (commented out for safety)
        # if documents.documents:
        #     doc_to_delete = documents.documents[0]
        #     print(f"Deleting document: {doc_to_delete.name}")
        #     client.delete_document(
        #         collection_id=collection.id,
        #         document_id=doc_to_delete.id,
        #         soft_delete=True
        #     )
        #     print("Document deleted (soft delete)")
        
        print("Document management operations available:")
        print("  - delete_document() for individual document removal")
        print("  - delete_collection() for entire collection removal")
        print("  - Both support soft delete (recoverable) and hard delete")
        
        print("\n✅ Vector Store example completed successfully!")
        print(f"Collection '{collection.title}' created with ID: {collection.id}")
        print("You can use this collection ID for further experiments.")
        
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