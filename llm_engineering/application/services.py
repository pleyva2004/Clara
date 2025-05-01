from ..model.operations import readEmailLLM, createMessageLLM, validateMessageLLM, classifyEmail



class Clara:
    
    def __init__(self):
        print("Clara is being initialized")

    def classifyEmail(self, sender: str, subject: str, body_snippet: str):
        print("Classifying email...")
        response = classifyEmail(sender, subject, body_snippet)
        return response
    
    def readEmail(self, input_email: str):
        print("Reading email...")
        response = readEmailLLM(input_email)
        return response

    def createMessage(self, input_email_summary: str):
        print("Creating message for Whatsapp...")
        response = createMessageLLM(input_email_summary)
        return response
    
    def validateMessage(self, input_message: str, input_email_summary: str, input_email: str):
        print("Validating message...")
        response = validateMessageLLM(input_message, input_email_summary, input_email)
        return response

    def createEmail(self):
        print("Creating email...")
    
    def validateEmail(self):
        print("Validating email...")

        
        