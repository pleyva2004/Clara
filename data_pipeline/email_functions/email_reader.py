from imap_tools import MailBox
import re


def getEmail(email_address: str, password: str, imap_server: str = "imap.gmail.com"):

    # Get date, subject and body len of all emails from INBOX folder
    with MailBox(imap_server).login(email_address, password) as mailbox:
        for msg in mailbox.fetch(limit=1, reverse=True):
            body = ''
            
            if "Re: " in msg.subject:
                print("Response Email...")
                # print(msg.subject)
            else:
                print("SHPE Email...")
        

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
            # print(array)

            length = len(array)
            # Initiate index
            i = 0 
            # Initiate index for reverse
            j = 0

            signature_found = False
            while i < length:
                # Iterate through the array in reverse order
                j = length - i - 1
                line = array[j]

                # Check for signature pattern (1-2 words followed by comma and carriage return)
                if re.search(r'^\w+(?:\s+\w+)?,\r$', line) or re.search(r'^-- \r', line):
                    print('Signature found')
                    signature_found = True
                    break
                i += 1

            # After signature is found, iterate through the array in forward order
            if not signature_found:
                j = length

            # Line index for Iterate through the array in forward order
            for line in range(j):
                line = array[line]
                body += line[:-1] + " "

            dict = {
                "Company": "SHPE",
                "Sender": msg.from_,
                "Subject": msg.subject,
                "Email_Contents": body,
                "Attachments": [] #
            }
            return dict