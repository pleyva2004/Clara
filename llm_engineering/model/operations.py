from .gemini_provider import GeminiClient
from google.genai.types import Tool, FunctionDeclaration
from ..infrastructure import readEmailPrompt, createMessagePrompt, validateMessagePrompt, emailClassifierPrompt, validateResponsePrompt


def classifyEmailLLM(sender: str, subject: str, body_snippet: str) -> str:
    client = GeminiClient()
    prompt = emailClassifierPrompt(sender, subject, body_snippet)
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

    # Create Tool with FunctionDeclaration
    tool = Tool(function_declarations=[FunctionDeclaration(**classify_email_declaration)])
    tools = [{"function_declarations": [classify_email_declaration]}]
    
    try:
        response = client.generate_text(
            prompt,
            system_instruction,
            temperature=0.1,
            top_p=0.3,
            top_k=3,
            tools=[{"function_declarations": [classify_email_declaration]}]
        )
        return response
    except Exception as e:
        print(f"Error classifying email: {e}")
        return "Clara was unable to classify the email. Please try again."

def readEmailLLM(email: str) -> str:
    client = GeminiClient()
    prompt = readEmailPrompt(email)
    # system_instruction = "You are a helpful email reader. Be simple and concise."
    try:
        response = client.generate_text(prompt)
        return response
    except Exception as e:
        print(f"Error reading email: {e}")
        return "Clara was unable to read the email. Please try again."

def createMessageLLM(email_summary: str) -> str:
    client = GeminiClient()
    prompt = createMessagePrompt(email_summary)
    system_instruction = "You are a secretary that creates messages for Whatsapp groups.  "
    try:
        response = client.generate_text(prompt, system_instruction, temperature=0.3)
        return response
    except Exception as e:
        print(f"Error creating message: {e}")
        return "Clara was unable to create a message. Please try again."

def validateMessageLLM(message: str, email_summary: str, email: str) -> str:
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

    # Create Tool with FunctionDeclaration
    tool = Tool(function_declarations=[FunctionDeclaration(**validate_message_declaration)])
    tools = [{"function_declarations": [validate_message_declaration]}]

    try:
        response = client.generate_text(
            prompt,
            system_instruction,
            temperature=0.1,
            top_p=0.3,
            top_k=10,
            tools=[{"function_declarations": [validate_message_declaration]}]
        )
        return response
    except Exception as e:
        print(f"Error validating message: {e}")
        return "Clara was unable to validate the message. Please try again."

def validateResponseLLM(response: str, message: str) -> str:
    client = GeminiClient()
    prompt = validateResponsePrompt(response, message)
    system_instruction = "You are a precise action item validator. Your task is to check if a response addresses all the action items mentioned in a message."

    # Define the function declaration with correct type values
    validate_message_response_declaration = {
        "name": "validate_message_response",
        "description": "Validates a response against action items in the message",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "accuracy_score": {
                    "type": "NUMBER",
                    "description": "Accuracy score from 0-100 based on how many action items were addressed"
                },
                "action_items_in_message": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "List of action items extracted from the message"
                },
                "action_items_addressed": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "List of action items that were addressed in the response"
                },
                "missing_information": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "List of action items NOT addressed in the response"
                },
                "suggested_corrections": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "List of specific suggestions to address missing items"
                }
            },
            "required": ["accuracy_score"]
        }
    }

    # Create Tool with FunctionDeclaration
    tool = Tool(function_declarations=[FunctionDeclaration(**validate_message_response_declaration)])
    tools = [{"function_declarations": [validate_message_response_declaration]}]

    try:
        response = client.generate_text(
            prompt,
            system_instruction,
            temperature=0.1,
            top_p=0.3,
            top_k=10,
            tools=[{"function_declarations": [validate_message_response_declaration]}]
        )
        return response
    except Exception as e:
        print(f"Error validating message response: {e}")
        return "Clara was unable to validate the message response. Please try again."