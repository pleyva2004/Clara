import imaplib
import time
import os
from dotenv import load_dotenv


def check_new_emails(email_address: str, password: str, imap_server: str = "imap.gmail.com") -> bool:
    """
    Check for new emails in the specified inbox.
    
    Args:
        email_address (str): The email address to check
        password (str): The password or app-specific password for the email account
        imap_server (str): The IMAP server address (defaults to Gmail's IMAP server)
    
    Returns:
        bool: True if new emails are found, False otherwise
    """
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)
        
        # Login to the account
        mail.login(email_address, password)
        
        # Select the inbox
        mail.select("inbox")
        
        # Search for all unread emails using the correct IMAP search criteria
        status, messages = mail.search(None, "(UNSEEN)")
        
        if status != 'OK':
            print(f"Error searching emails: {status}")
            return False
            
        # Get the list of message numbers
        message_numbers = messages[0].split()
        
        # Get the number of unread messages
        unread_count = len(message_numbers)
        
        # Close the connection
        mail.close()
        mail.logout()
        
        # Return True if there are unread messages
        return unread_count > 0
        
    except Exception as e:
        print(f"Error checking emails: {str(e)}")
        return False

def monitor_inbox(email_address: str, password: str, check_interval: int = 60) -> bool:
    """
    Continuously monitor the inbox for new emails.
    
    Args:
        email_address (str): The email address to monitor
        password (str): The password or app-specific password for the email account
        check_interval (int): Time in seconds between checks (default: 60 seconds)
    
    Returns:
        bool: True when new email is detected, False otherwise
    """
    # print(f"Starting to monitor inbox for {email_address}")
    
    while True:
        if check_new_emails(email_address, password):
            # print("New email detected!")
            return True
        time.sleep(check_interval)

if __name__ == "__main__":
    load_dotenv()
    # Example usage
    EMAIL_ADDRESS = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")
    
    if not EMAIL_ADDRESS or not PASSWORD:
        print("Error: MAIL_USERNAME and MAIL_PASSWORD environment variables must be set")
        exit(1)
    
    # For continuous monitoring
    monitor_inbox(EMAIL_ADDRESS, PASSWORD)
    
    # # For single check
    # has_new_emails = check_new_emails(EMAIL_ADDRESS, PASSWORD)
    # print(f"Has new emails: {has_new_emails}")




