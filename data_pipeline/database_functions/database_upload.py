import json
from data_pipeline.database_functions import get_connection

# Takes the already parsed data and puts it into the database
'''
Takes 2 parameters: 
    conn: The connection function status which checks to see if we connected to the database
    file_path: The path of the json file to be inserted into the database
'''
def extract(conn, file_path):
    if conn == None:
        return "Connection Failed"
    
    try:
        # Try and open Json file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract the data form the Json file
        body = data.get("Body", {})
        sender = body.get("Sender")
        subject = body.get("Subject")
        email_contents = body.get("Email_Contents")
        attachments = body.get("Attachments")
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO Email_Inbox (sender, subject, email_content, attachments)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_query, (sender, subject, email_contents, attachments))
        conn.commit() # Save the changes
        print("Data transfer Successful")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print("Database connection closed")


json_file_path = "/home/lior/GitRepo/Clara/data_pipeline/Tests/temp.json" # Must give a path the the 
conn = get_connection("sql1.njit.edu", "lb356", "123Luigi895@", "lb356") 
extract(conn, json_file_path)
