from .gemini_provider import GeminiClient
from google.genai.types import Tool, FunctionDeclaration
from ..infrastructure.prompts import readEmailPrompt, createMessagePrompt, validateMessagePrompt, emailClassifierPrompt, validateResponsePrompt, editMessagePrompt, requestMissingInformationPrompt


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
    system_instruction = "You are a precise email reader. You carefully process the email and you never miss information. Your task is to extract ALL information from the email, including dates, names, action items, and any other relevant details. Be thorough and complete in your extraction."
    try:
        response = client.generate_text(
            prompt, 
            system_instruction,
            temperature=0.1,  # Lower temperature for more precise extraction
            top_p=0.3,
            top_k=10
        )
        return response
    except Exception as e:
        print(f"Error reading email: {e}")
        return "Clara was unable to read the email. Please try again."

def createMessageLLM(email_summary: str) -> str:
    client = GeminiClient()
    prompt = createMessagePrompt(email_summary)
    system_instruction = "You are CLARA. You are having a conversation with a member of the organizaiton. You are the secretary of the organization. Your task is to create a message for the group."
    try:
        response = client.generate_text(prompt, system_instruction, temperature=0.3)
        return response
    except Exception as e:
        print(f"Error creating message: {e}")
        return "Clara was unable to create a message. Please try again."

def validateMessageLLM(message: str, email_summary: str, email: str) -> str:
    client = GeminiClient()
    prompt = validateMessagePrompt(message, email_summary, email)
    # system_instruction = "You are a precise fact-checker. Your task is to validate the accuracy of a WhatsApp message against its source email and summary."
    
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
            # system_instruction,
            temperature=0.1,
            top_p=0.3,
            top_k=10,
            tools=[{"function_declarations": [validate_message_declaration]}]
        )
        return response
    except Exception as e:
        print(f"Error validating message: {e}")
        return "Clara was unable to validate the message. Please try again."

def editMessageLLM(message: str, edits: str, context: str) -> str:
    client = GeminiClient()
    prompt = editMessagePrompt(message, edits, context)
    system_instruction = "You are a precise message editor. You work with extreme diligence and your biggest strength is your attention to detail. Your task is to edit a message to make the necessary changes. Return ONLY the new edited message and nothing else. Do not include any other text or comments. Ensure that every edit is made to create a new message."
    try:
        response = client.generate_text(prompt, system_instruction, temperature=0.3)
        return response
    except Exception as e:
        print(f"Error editing message: {e}")
        return "Clara was unable to edit the message. Please try again."
    
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

def requestMissingInformationLLM(response: str, action_items_in_message: str, action_items_addressed: str, missing_information: str, suggested_corrections: str) -> str:
    client = GeminiClient()
    prompt = requestMissingInformationPrompt(response, action_items_in_message, action_items_addressed, missing_information, suggested_corrections)
    system_instruction = "You are CLARA. You are having a conversation with a member of the organizaiton. He has responses to your initial message. Your task is to request the missing information from the user. Return ONLY the new edited response and nothing else. Do not include any other text or comments."
    try:
        response = client.generate_text(
            prompt, 
            temperature=0.3,
        )
        return response
    except Exception as e:
        print(f"Error editing response: {e}")
        return "Clara was unable to response. Please try again."
