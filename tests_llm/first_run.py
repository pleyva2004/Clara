# main.py
from llm_engineering import Clara
import json 

def main():
    # Using generate_text - gets complete response at once
    client = Clara()
    email = open("tests/email.txt", "r").read()
    full_response = client.readEmail(email)
    message = client.createMessage(full_response)
    validation = client.validateMessage(message, full_response, email)
    
    # Save validation results to JSON file
    # First ensure we have a proper dictionaryS
    if isinstance(validation, str):
        validation_json = json.loads(validation.replace('```json\n', '').replace('\n```', ''))
    
    print(json.dumps(validation_json, indent=4))

if __name__ == "__main__":
    main()