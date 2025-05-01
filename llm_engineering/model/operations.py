from .gemini_provider import GeminiClient
from google.genai.types import Tool
from ..infrastructure import readEmailPrompt, createMessagePrompt, validateMessagePrompt, email_classifier_prompt


def classifyEmail(sender: str, subject: str, body_snippet: str) -> str:
    client = GeminiClient()
    prompt = email_classifier_prompt(sender, subject, body_snippet)
    system_instruction = "You are a precise email classifier. Your task is to classify the email into one of the following categories: Alumni, Company, Internal NJIT Partner, Unrelated. Return only the category and nothing else."
    
        # Define the function declaration with correct type values
    classify_email_declaration = {
        "name": "classify_email",
        "description": "Classifies an email into one of the following categories: Alumni, Company, Internal NJIT Partner, Unrelated.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": "The category of the email"
                },
                "meta_data": {
                    "type": "STRING",
                    "description": "If the email is related to a company, the meta data should be the company name. If the email is related to an alumni, the meta data should be the alumni name. If the email is related to an internal NJIT partner, the meta data should be the partner name. If the email is unrelated, the meta data should be 'Unrelated'."
                }
            },
            "required": ["category", "meta_data"]
        }
    }

    # Create the Tool object with the function declaration
    tools = [Tool(function_declarations=[classify_email_declaration])]
    
    try:
        response = client.generate_text(
            prompt,
            system_instruction,
            temperature=0.1,
            top_p=0.3,
            top_k=3,
            tools=tools
        )
        return response
    except Exception as e:
        print(f"Error classifying email: {e}")
        return None


def readEmailLLM(email: str) -> str:
    client = GeminiClient()
    prompt = readEmailPrompt(email)
    # system_instruction = "You are a helpful email reader. Be simple and concise."
    try:
        response = client.generate_text(prompt)
        return response
    except Exception as e:
        print(f"Error reading email: {e}")
        return None

def createMessageLLM(email_summary: str) -> str:
    client = GeminiClient()
    prompt = createMessagePrompt(email_summary)
    system_instruction = "You are a secretary that creates messages for Whatsapp groups.  "
    try:
        response = client.generate_text(prompt, system_instruction, temperature=0.3)
        return response
    except Exception as e:
        print(f"Error creating message: {e}")

def validateMessageLLM(message: str, email_summary: str, email: list) -> str:
    client = GeminiClient()
    prompt = validateMessagePrompt(message, email_summary, email)
    system_instruction = "You are a precise fact-checker. Your task is to validate the accuracy of a WhatsApp message against its source email and summary."
    
    # Define the function declaration with correct type values
    validate_message_declaration = {
        "name": "validate_message",
        "description": "Validates a message against source information",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "accuracy_score": {
                    "type": "NUMBER",
                    "description": "Accuracy score from 0-100"
                },
                "factual_discrepancies": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "List of any factual discrepancies found"
                },
                "missing_information": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "List of any critical missing information"
                },
                "format_compliant": {
                    "type": "BOOLEAN",
                    "description": "Whether the message follows required format"
                },
                "suggested_corrections": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "List of suggested corrections if needed"
                }
            },
            "required": ["accuracy_score", "format_compliant"]
        }
    }

    # Create the Tool object with the function declaration
    tools = [Tool(function_declarations=[validate_message_declaration])]

    try:
        response = client.generate_text(
            prompt,
            system_instruction,
            temperature=0.1,
            top_p=0.3,
            top_k=10,
            tools=tools
        )
        return response
    except Exception as e:
        print(f"Error validating message: {e}")

