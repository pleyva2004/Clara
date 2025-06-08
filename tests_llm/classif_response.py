from llm_engineering import Clara
import json

def main():
    client = Clara()
    email = open("tests_llm/email2.txt", "r").read()
    response = open("tests_llm/response.txt", "r").read()
    email_summary = client.readEmail(email)
    print("--------------------------------")
    print(email_summary)
    print("--------------------------------")
    message = client.createMessage(email_summary)
    print(message)
    validation = client.validateMessage(message, email_summary, email)
    print("--------------------------------")
    print(response)
    print("--------------------------------")
    classification = client.validateResponse(response, message)

    if isinstance(classification, str) or isinstance(validation, str):
        validation_json = json.loads(validation.replace('```json\n', '').replace('\n```', '').replace('```', '')) if validation else None
        classification_json = json.loads(classification.replace('```json\n', '').replace('\n```', '').replace('```', '')) if classification else None
    
    print(json.dumps(validation_json, indent=4))
    print("--------------------------------")
    print(json.dumps(classification_json, indent=4))

if __name__ == "__main__":
    main()