from llm_engineering import Clara
import json

def main():

    # Setup 
    client = Clara()
    email = open("tests_llm/email2.txt", "r").read()
    response = open("tests_llm/response.txt", "r").read()
    email_summary = client.readEmail(email)
    print("--------------------------------")
    print(email_summary)
    print("--------------------------------")
    message = client.createMessage(email_summary)
    print(message)
    validate_clara_message = client.validateMessage(message, email_summary, email)
    print("--------------------------------")
    print(response)
    print("--------------------------------")
    validate_user_response = client.validateResponse(response, message)

    if isinstance(validate_clara_message, str) or isinstance(validate_user_response, str):
        validate_clara_message_json = json.loads(validate_clara_message.replace('```json\n', '').replace('\n```', '').replace('```', '')) 
        validate_user_response_json = json.loads(validate_user_response.replace('```json\n', '').replace('\n```', '').replace('```', '')) 
    
    missing_information = validate_clara_message_json["missing_information"][0]
    suggested_corrections = validate_clara_message_json["suggested_corrections"][0]
    message_score = validate_clara_message_json["accuracy_score"]

    action_items_in_message = validate_user_response_json["action_items_in_message"][0]
    action_items_addressed = validate_user_response_json["action_items_addressed"][0]
    missing_information_for_response = validate_user_response_json["missing_information"][0]
    suggested_corrections_for_response = validate_user_response_json["suggested_corrections"][0]
    response_score = validate_user_response_json["accuracy_score"]

    print("--------------------------------")
    print(json.dumps(validate_clara_message_json, indent=4))
    print("--------------------------------")
    print(json.dumps(validate_user_response_json, indent=4))
    print("--------------------------------")

    print(f"Missing Information: {missing_information}")
    print(f"Suggested Corrections: {suggested_corrections}")
    print(f"Message Score: {message_score}")

    if message_score < 90:
        edited_message = client.editMessage(message, suggested_corrections, missing_information)
        print("--------------------------------")
        print(edited_message)
        print("--------------------------------")
        validate_edited_message = client.validateMessage(edited_message, email_summary, email)
        validate_edited_message_json = json.loads(validate_edited_message.replace('```json\n', '').replace('\n```', '').replace('```', ''))

        print("--------------------------------")
        print(json.dumps(validate_edited_message_json, indent=4))
        print("--------------------------------")

    print("--------------------------------")
    print(f"Action Items in Message: {action_items_in_message}")
    print(f"Action Items Addressed: {action_items_addressed}")
    print(f"Missing Information for Response: {missing_information_for_response}")
    print(f"Suggested Corrections for Response: {suggested_corrections_for_response}")
    print(f"Response Score: {response_score}")
    print("--------------------------------")

    if response_score < 90:
        clara_request_missing_information = client.requestMissingInformation(response, action_items_in_message, action_items_addressed, missing_information_for_response, suggested_corrections_for_response)
        print("--------------------------------")
        print(clara_request_missing_information)
        print("--------------------------------")

if __name__ == "__main__":
    main()