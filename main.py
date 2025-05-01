from data_pipeline.email_functions import monitor_inbox, getEmail
from llm_engineering import Clara

from dotenv import load_dotenv
import os
import json

def main():
    load_dotenv()
    EMAIL_ADDRESS = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")
    print(f"Starting to monitor inbox for {EMAIL_ADDRESS}")
    
    if monitor_inbox(EMAIL_ADDRESS, PASSWORD):
        print("New email detected!")
        print("Reading email...")
        email_data = getEmail(EMAIL_ADDRESS, PASSWORD)
        
        # Convert to JSON
        json_data = json.dumps(email_data, indent=4, ensure_ascii=False)
        print("Email data as JSON:")
        
        print(json_data)
        print("Email read and converted successfully!")

        # Call Email Classifier HERE

        client = Clara()
        sender = email_data["Sender"]
        subject = email_data["Subject"]
        email = email_data["Email_Contents"]
        classification = client.classifyEmail(sender, subject, email)

        if isinstance(classification, str):
            classification_json = json.loads(classification.replace('```json\n', '').replace('\n```', ''))
        
        print(json.dumps(classification_json, indent=4))

        # Call the DATA BASE FUNCTIONs HERE

        # Call CLARA HERE


if __name__ == "__main__":
    main()


