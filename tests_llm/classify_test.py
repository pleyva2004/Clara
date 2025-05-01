from llm_engineering import Clara
import json

def main():
    client = Clara()
    email = open("tests/email.txt", "r").read()
    sender = "anthony.vaccarino@pgim.com"
    subject = "SHPE PGIM Fixed Income - Fall 2025 Recruiting Engagement"
    classification = client.classifyEmail(sender, subject, email)

    if isinstance(classification, str):
        classification_json = json.loads(classification.replace('```json\n', '').replace('\n```', ''))
    
    print(json.dumps(classification_json, indent=4))

if __name__ == "__main__":
    main()