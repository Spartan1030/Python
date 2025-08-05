#!/usr/bin/env python3
"""
Prompt Store focused example for GE HealthCare IDS SDK.

This example demonstrates comprehensive prompt template management:
1. Creating prompt templates with validation
2. Version management and lifecycle
3. Setting default versions with justification
4. Advanced querying and filtering
5. Template cloning and modification
6. Best practices for prompt organization
"""

from gehc_ids import PromptStoreClient, IDSAuth
from gehc_ids.exceptions import IDSException


def main():
    """Main example function."""
    
    # Initialize authentication and client
    auth = IDSAuth(
        client_id="your-client-id",
        client_secret="your-client-secret",
        audience="your-audience-id"
    )
    
    client = PromptStoreClient(auth=auth)
    
    try:
        # 1. Health check
        print("🔍 Checking Prompt Store service...")
        health = client.health_check()
        print(f"Status: {health.status} - {health.message}")
        
        # 2. Create comprehensive prompt templates
        print("\n📝 Creating Prompt Templates")
        print("-" * 40)
        
        # Medical summarization prompt
        print("Creating medical summarization prompt...")
        medical_prompt = client.create_prompt_template(
            name="Medical_Document_Summarizer",
            content="""You are a medical AI assistant specialized in clinical documentation.

Context: {context}

Task: Please provide a comprehensive medical summary addressing the following question: {question}

Guidelines:
- Use precise medical terminology
- Include relevant diagnostic information
- Highlight key clinical findings
- Provide actionable insights when appropriate
- Maintain professional medical tone

Summary:""",
            type="System",
            provider="OpenAI",
            params='{"model": "gpt-4", "temperature": 0.3, "max_tokens": 500, "top_p": 0.9}',
            category="summarization",
            tags=["medical", "clinical", "summary", "healthcare"]
        )
        print(f"Created: {medical_prompt.name} v{medical_prompt.version}")
        
        # Patient education prompt
        print("\nCreating patient education prompt...")
        education_prompt = client.create_prompt_template(
            name="Patient_Education_Assistant",
            content="""You are a patient education specialist. Your role is to explain medical information in simple, understandable terms.

Medical Context: {context}

Patient Question: {question}

Instructions:
- Use simple, non-technical language
- Provide clear, accurate information
- Include practical advice when relevant
- Be empathetic and supportive
- Avoid giving specific medical advice
- Recommend consulting healthcare providers for personalized care

Response:""",
            type="System", 
            provider="OpenAI",
            params='{"model": "gpt-3.5-turbo", "temperature": 0.4, "max_tokens": 400}',
            category="education",
            tags=["patient", "education", "healthcare", "communication"]
        )
        print(f"Created: {education_prompt.name} v{education_prompt.version}")
        
        # Research analysis prompt
        print("\nCreating research analysis prompt...")
        research_prompt = client.create_prompt_template(
            name="Research_Paper_Analyzer",
            content="""You are a medical research analyst. Analyze the provided research context and answer questions with scientific rigor.

Research Context: {context}

Analysis Question: {question}

Analysis Framework:
- Evaluate methodology and evidence quality
- Identify key findings and statistical significance
- Assess clinical relevance and implications
- Note limitations and potential biases
- Provide evidence-based conclusions

Analysis:""",
            type="System",
            provider="OpenAI", 
            params='{"model": "gpt-4", "temperature": 0.2, "max_tokens": 600, "top_p": 0.8}',
            category="analysis",
            tags=["research", "analysis", "evidence", "clinical-trials"]
        )
        print(f"Created: {research_prompt.name} v{research_prompt.version}")
        
        # 3. Version management workflow
        print("\n🔄 Version Management Workflow")
        print("-" * 40)
        
        # Create improved version of medical summarizer
        print("Creating improved version of medical summarizer...")
        medical_v2 = client.create_prompt_version(
            name="Medical_Document_Summarizer",
            content="""You are an expert medical AI assistant with specialized training in clinical documentation and evidence-based medicine.

Clinical Context: {context}

Clinical Question: {question}

Analysis Requirements:
- Apply evidence-based medical principles
- Include relevant ICD-10 codes when applicable
- Provide differential diagnosis considerations
- Highlight red flags or urgent findings
- Include follow-up recommendations
- Maintain HIPAA compliance and patient confidentiality

Clinical Summary:""",
            params='{"model": "gpt-4-turbo", "temperature": 0.25, "max_tokens": 700, "top_p": 0.85}',
            tags=["medical", "clinical", "evidence-based", "icd10", "hipaa"]
        )
        print(f"Created version {medical_v2.version} with enhanced clinical focus")
        
        # Create specialized version for emergency medicine
        print("\nCreating emergency medicine specialized version...")
        emergency_v3 = client.create_prompt_version(
            name="Medical_Document_Summarizer", 
            content="""You are an emergency medicine AI assistant trained in rapid clinical assessment and triage protocols.

Emergency Context: {context}

Urgent Question: {question}

Emergency Assessment Protocol:
- Prioritize life-threatening conditions (ABC assessment)
- Apply emergency triage protocols (ESI levels)
- Identify immediate interventions required
- Consider time-sensitive diagnoses
- Include stabilization measures
- Provide clear disposition recommendations

Emergency Assessment:""",
            params='{"model": "gpt-4", "temperature": 0.1, "max_tokens": 400, "top_p": 0.7}',
            category="emergency",
            tags=["emergency", "triage", "urgent", "stabilization", "esi"]
        )
        print(f"Created version {emergency_v3.version} for emergency medicine")
        
        # 4. Set default versions with justification
        print("\n⭐ Managing Default Versions")
        print("-" * 40)
        
        # Set the enhanced version as default
        print("Setting enhanced clinical version as default...")
        client.set_default_version(
            name="Medical_Document_Summarizer",
            version=medical_v2.version,
            justification="Enhanced version includes ICD-10 coding, evidence-based analysis, and improved clinical structure"
        )
        print(f"Version {medical_v2.version} set as default")
        
        # 5. Comprehensive prompt querying
        print("\n🔍 Prompt Discovery and Management")
        print("-" * 40)
        
        # List all prompts
        print("Listing all prompt templates...")
        all_prompts = client.get_all_prompts(page=1, size=20)
        print(f"Total prompts found: {all_prompts.total_count}")
        
        for prompt in all_prompts.prompts:
            default_marker = " (DEFAULT)" if prompt.default else ""
            print(f"  - {prompt.name} v{prompt.version}{default_marker}")
            print(f"    Category: {prompt.category}, Provider: {prompt.provider}")
            if prompt.tags:
                print(f"    Tags: {', '.join(prompt.tags)}")
        
        # Get all versions of a specific prompt
        print(f"\nAnalyzing versions of '{medical_prompt.name}'...")
        versions = client.get_prompt_versions("Medical_Document_Summarizer")
        print(f"Found {len(versions.prompts)} versions:")
        
        for version in versions.prompts:
            default_marker = " (DEFAULT)" if version.default else ""
            print(f"  Version {version.version}{default_marker}:")
            print(f"    Category: {version.category}")
            print(f"    Tags: {', '.join(version.tags) if version.tags else 'None'}")
            print(f"    Content preview: {version.content[:100]}...")
        
        # 6. Advanced filtering and search
        print("\n🎯 Advanced Filtering Examples")
        print("-" * 40)
        
        # Filter by category
        print("Prompts in 'summarization' category:")
        summary_prompts = client.get_all_prompts(category="summarization")
        for prompt in summary_prompts.prompts:
            print(f"  - {prompt.name} v{prompt.version}")
        
        # Filter by provider
        print("\nPrompts using GPT-4:")
        gpt4_prompts = client.get_all_prompts(provider="OpenAI")
        for prompt in gpt4_prompts.prompts:
            # Check if GPT-4 is mentioned in params
            if "gpt-4" in str(prompt.params).lower():
                print(f"  - {prompt.name} v{prompt.version}")
        
        # Filter by tags
        print("\nPrompts tagged with 'medical':")
        medical_prompts = client.get_all_prompts(tag="medical")
        for prompt in medical_prompts.prompts:
            print(f"  - {prompt.name} v{prompt.version}")
        
        # 7. Template retrieval examples
        print("\n📖 Template Retrieval Examples")
        print("-" * 40)
        
        # Get default version
        default_medical = client.get_default_prompt("Medical_Document_Summarizer")
        print(f"Default version of Medical_Document_Summarizer: v{default_medical.version}")
        
        # Get latest version
        latest_medical = client.get_latest_prompt("Medical_Document_Summarizer")
        print(f"Latest version of Medical_Document_Summarizer: v{latest_medical.version}")
        
        # Get specific version
        specific_version = client.get_prompt_version("Medical_Document_Summarizer", 1)
        print(f"Original version content preview: {specific_version.content[:80]}...")
        
        # 8. Template cloning and modification
        print("\n🔄 Template Cloning and Customization")
        print("-" * 40)
        
        # Clone the patient education prompt for pediatric use
        print("Cloning patient education prompt for pediatric use...")
        pediatric_prompt = client.clone_prompt_template(
            source_name="Patient_Education_Assistant",
            target_name="Pediatric_Education_Assistant",
            source_version="default",
            modifications={
                "content": """You are a pediatric patient education specialist. Explain medical information in age-appropriate language for children and their families.

Medical Context: {context}

Family Question: {question}

Guidelines:
- Use age-appropriate language and concepts
- Include analogies and simple explanations
- Address both child and parent/caregiver concerns
- Provide reassurance and comfort
- Include family-friendly resources when relevant
- Consider developmental stages in explanations

Child-Friendly Response:""",
                "tags": ["pediatric", "family", "child-friendly", "education"],
                "category": "pediatric-education"
            }
        )
        print(f"Created pediatric variant: {pediatric_prompt.name}")
        
        # 9. Prompt lifecycle management
        print("\n🗂️ Prompt Lifecycle Management")
        print("-" * 40)
        
        # Create a test prompt for demonstration
        test_prompt = client.create_prompt_template(
            name="Test_Prompt_Demo",
            content="Test context: {context}\nTest question: {question}\nTest response:",
            category="testing",
            tags=["test", "demo"]
        )
        print(f"Created test prompt: {test_prompt.name}")
        
        # Create multiple versions
        for i in range(2, 4):
            client.create_prompt_version(
                name="Test_Prompt_Demo",
                content=f"Updated test context v{i}: {{context}}\nUpdated question v{i}: {{question}}\nResponse v{i}:",
                tags=["test", "demo", f"version-{i}"]
            )
            print(f"Created version {i}")
        
        # Demonstrate version deletion
        print("Deleting version 2...")
        client.delete_prompt_version("Test_Prompt_Demo", 2)
        print("Version 2 deleted")
        
        # Show remaining versions
        remaining_versions = client.get_prompt_versions("Test_Prompt_Demo")
        print(f"Remaining versions: {[p.version for p in remaining_versions.prompts]}")
        
        # 10. Best practices demonstration
        print("\n💡 Best Practices Summary")
        print("-" * 40)
        
        # Get all prompt names for organization
        prompt_names = client.list_prompt_names()
        print(f"Total unique prompt templates: {len(prompt_names)}")
        print("Prompt template names:")
        for name in prompt_names:
            print(f"  - {name}")
        
        # Organization by category
        all_prompts_final = client.get_all_prompts()
        categories = {}
        for prompt in all_prompts_final.prompts:
            cat = prompt.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(prompt.name)
        
        print("\nPrompts organized by category:")
        for category, prompts in categories.items():
            unique_prompts = list(set(prompts))
            print(f"  {category}: {len(unique_prompts)} templates")
            for prompt_name in unique_prompts[:3]:  # Show first 3
                print(f"    - {prompt_name}")
            if len(unique_prompts) > 3:
                print(f"    ... and {len(unique_prompts) - 3} more")
        
        print("\n✅ Prompt Store example completed successfully!")
        print("\nKey takeaways:")
        print("- Always include {context} and {question} variables in prompt content")
        print("- Use semantic versioning and meaningful version descriptions")
        print("- Organize prompts with consistent naming conventions")
        print("- Leverage tags for efficient discovery and filtering")
        print("- Set appropriate default versions with clear justification")
        print("- Clone and modify existing prompts for specialized use cases")
        
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