import json
import re
from connect import get_connection

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
        email_contents = body.get("Email_Contents", "No Conntent")
        attachments = body.get("Attachments", "No Attachments")


        # Grab company from Json
        raw_partner = body.get("Partner")
        
        # Remove special characters from the company name
        table_name = re.sub(r'\W+', '_', raw_partner).lower()
        cursor = conn.cursor()

        # If the table does not exist, create it
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            sender TEXT,
            subject TEXT,
            email_content TEXT,
            attachments TEXT
        )
        """
        cursor.execute(create_table_query)
        
        #insert the data into the table
        insert_query = f"""
        INSERT INTO {table_name} (sender, subject, email_content, attachments)
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


json_file_path = "/home/lior/GitRepo/Clara/data_pipeline/Tests/test2.json" # Must give a path the the 
conn = get_connection("sql1.njit.edu", "lb356", "123Luigi895@", "lb356") 
extract(conn, json_file_path)
