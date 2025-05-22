from create_connection import connect_telegram
from create_chat import create_group
from add_users import add_users_to_group
if __name__ == "__main__":
    app_id = 24829326
    api_hash = '4bc9bc068c98b8ed0ad8841e410a64a1'
    session_name = 'session_name'
    group_name = 'Clara Test'
    intial_users = ['@liorbiton']
    more_users = []

    print("connecting to telegram...")
    client = connect_telegram(session_name, app_id, api_hash)

    print("creating group...")
    group = create_group(client,group_name, intial_users)

    if group:
        print("adding more users...")
        add_users_to_group(client, group, more_users)