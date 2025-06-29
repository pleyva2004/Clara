from ..model import readEmailLLM, createMessageLLM, validateMessageLLM, classifyEmailLLM, validateResponseLLM, editMessageLLM, requestMissingInformationLLM



class Clara:
    
    def __init__(self):
        print("Clara is being initialized")

    def classifyEmail(self, sender: str, subject: str, body_snippet: str):
        print("Classifying email...")
        response = classifyEmailLLM(sender, subject, body_snippet)
        return response
    
    def readEmail(self, input_email: str):
        print("Reading email...")
        response = readEmailLLM(input_email)
        return response

    def createMessage(self, input_email_summary: str):
        print("Creating message for Telegram...")
        response = createMessageLLM(input_email_summary)
        return response
    
    def validateMessage(self, input_message: str, input_email_summary: str, input_email: str):
        print("Validating message...")
        response = validateMessageLLM(input_message, input_email_summary, input_email)
        return response
    
    def editMessage(self, input_message: str, input_edits: str, input_context: str):
        print("Editing message...")
        response = editMessageLLM(input_message, input_edits, input_context)
        return response

    def validateResponse(self, input_response: str, input_message: str):
        print("Validating response...")
        response = validateResponseLLM(input_response, input_message)
        return response
    
    def requestMissingInformation(self, input_response: str, input_action_items_in_message: str, input_action_items_addressed: str, input_missing_information: str, input_suggested_corrections: str):
        print("Requesting missing information...")
        response = requestMissingInformationLLM(input_response, input_action_items_in_message, input_action_items_addressed, input_missing_information, input_suggested_corrections)
        return response
    
    def createEmail(self):
        print("Creating email...")
    
    def validateEmail(self):
        print("Validating email...")

        
        