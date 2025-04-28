from imap_tools import MailBox
import re

MAIL_PASSWORD = "gwjamkdovezjlfho" 
MAIL_USERNAME = "njitshpe@gmail.com"

def get_email_from():
    # Get date, subject and body len of all emails from INBOX folder
    with MailBox('imap.gmail.com').login(MAIL_USERNAME, MAIL_PASSWORD) as mailbox:
        for msg in mailbox.fetch(limit=1, reverse=True):
            print("Email found and parsing...")
            body = ''
            
            if "Re: " in msg.subject:
                print("Response Email...")
                # print(msg.subject)


                # Saving attachments into assets folder
                # for att in msg.attachments:
                    # Print attachment info
                    # print(f"Attachment name: {att.filename}")
                    # print(f"Attachment type: {att.content_type}")
                    
                    # # Save the attachment
                    # with open(f"downloads/{att.filename}", "wb") as f:
                    #     f.write(att.payload)
                    # print(f"Saved attachment: {att.filename}")
                                
                array = msg.text.split('\n')

                # Remove all lines that start with '>' or '>>' and filter out njitshpe/njit.edu lines
                array = [line for line in array if not (line.startswith('>') or 'njitshpe' in line or 'njit.edu' in line) and len(line) > 1]

                length = len(array)
                i = 0 
                while i < length:

                    # Iterate through the array in reverse order
                    line = array[length - i - 1]

                    # Check for any word followed by comma and carriage return
                    if re.search(r'\w+,\r', line):
                        print('Signature found')
                        break

                    i += 1

                updated_length = len(array)

                while i < updated_length:

                    # Iterate through the array in forward order
                    line = array[i]

                    print(line[:-1])
                    body += line[:-1] + " "

            elif "SHPE" in msg.subject or "SHPE" in msg.from_:
                print("SHPE Email...")
                # print(msg.subject)


                # Saving attachments into assets folder
                # for att in msg.attachments:
                    # Print attachment info
                    # print(f"Attachment name: {att.filename}")
                    # print(f"Attachment type: {att.content_type}")
                    
                    # # Save the attachment
                    # with open(f"downloads/{att.filename}", "wb") as f:
                    #     f.write(att.payload)
                    # print(f"Saved attachment: {att.filename}")

                    
                #PARSING MSG.TEXT
                array = msg.text.split('\n')

                # Remove all lines that start with '>' or '>>' and filter out njitshpe/njit.edu lines
                array = [line for line in array if not (line.startswith('>') or 'njitshpe' in line or 'njit.edu' in line) and len(line) > 1]
                
                length = len(array)
                for i in range(length):

                    # Iterate through the array in reverse order
                    line = array[length - i - 1]

                    if len(line) > 1:
                        array.pop(length - i - 1)

                        # Check for any word followed by comma and carriage return
                        if re.search(r'\w+,\r', line):
                            print('Signature found')
                            break
                        
                for i in range(len(array)):

                    # Iterate through the array in forward order
                    line = array[i]

                    # If the line does not contain 'njitshpe' or 'njit.edu' and is longer than 1 character
                    if len(line) > 1:
                        
                        print(line[:-1])
                        body += line[:-1] + " "

            return body, msg.from_, msg.subject    
print(get_email_from())