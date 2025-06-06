from data_pipeline.email_functions import monitor_inbox, getEmail
from data_pipeline.database_functions import extract, get_connection
from telegram_bot.create_connection import connect_telegram
from telegram_bot.send_messages import send_bot_message
from telegram_bot.group_exists import isGroup
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
        email_contents = email_data["Email_Contents"]
        classification = client.classifyEmail(sender, subject, email_contents)

        if isinstance(classification, str):
            classification_json = json.loads(classification.replace('```json\n', '').replace('\n```', ''))
        
        print(json.dumps(classification_json, indent=4))

        
        partner = classification_json["meta_data"]
        category = classification_json["category"]


        if category == "Unrelated":
            print("Email is unrelated to SHPE")
            print(email_contents)
            return 

        # Create final JSON
        final_json = {
            "Header": "parsed_email",
            "Body": {
                "Partner": partner,
                "Sender": sender,
                "Subject": subject,
                "Email_Contents": email_contents,
                "Attachments": "TBD"
            }
        }

        with open("./assets/temp.json", "w") as f:
            json.dump(final_json, f, indent=4)

        # Call the DATA BASE FUNCTIONS HERE
        json_file_path = "./assets/temp.json" # Must give a path the the 
        conn = get_connection("sql1.njit.edu", "lb356", "123Luigi895@", "lb356") 
        extract(conn, json_file_path)

        # Call CLARA HERE
        client = Clara()
        full_response = client.readEmail(email_contents)
        message = client.createMessage(full_response)
        print(message)
        validation = client.validateMessage(message, full_response, email_contents)
        
        # Save validation results to JSON file
        # First ensure we have a proper dictionaries
        if isinstance(validation, str):
            validation_json = json.loads(validation.replace('```json\n', '').replace('\n```', ''))
        
        print(json.dumps(validation_json, indent=4))

        # Send to Telegram Group
        app_id = os.getenv("TELEGRAM_API_ID")
        api_hash = os.getenv("TELEGRAM_API_HASH")
        session_name = 'session_name'
        group_name = 'Clara Test'
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")


        print("Connecting to telegram...")
        client = connect_telegram(session_name, app_id, api_hash)

        print("Checking group...")
        group = isGroup(client, group_name)

        chat_id = client.get_entity(group_name) # Gets the basic group id
        chat_id = "-100" + str(chat_id.id) # Add -100 because super group requires it
        
        # Send the message
        print("Sending Message...")
        send_bot_message(bot_token, chat_id, message)
        print(f"Message sent to {group!r}")


if __name__ == "__main__":
    main()


