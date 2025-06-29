from datetime import datetime
import json
import os
from data_pipeline.database_functions import get_connection
from dotenv import load_dotenv
load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# When Clara sends first message
def create_conversation_thread(thread_id, chat_id, bot_message, message_id, source_email_id):

    conn = get_connection(
        servername='sql1.njit.edu',
        username=DB_USERNAME,
        password=DB_PASSWORD,
        dbname='lb356'
    )
    
    cursor = conn.cursor()
    try:
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_threads (
                id INT AUTO_INCREMENT PRIMARY KEY,
                thread_id VARCHAR(255),
                chat_id BIGINT NOT NULL,
                user_id BIGINT,
                sender_role ENUM('user', 'bot') NOT NULL,
                message_text TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                telegram_message_id BIGINT NOT NULL,
                source_email_id VARCHAR(255),
                status ENUM('open', 'closed') NOT NULL DEFAULT 'open'
            )
        """)
        
        cursor.execute("""
            INSERT INTO conversation_threads (thread_id, chat_id, user_id, sender_role, message_text, timestamp, telegram_message_id, source_email_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (thread_id, chat_id, None, 'bot', bot_message, datetime.now(), message_id, source_email_id))

        conn.commit()
        print(f"[DB] Created new conversation thread: {thread_id} (open)")
    except Exception as e:
        print(f"[DB ERROR] Failed to create conversation thread: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def close_conversation_thread(thread_id):

    conn = get_connection(
        servername='sql1.njit.edu',
        username=DB_USERNAME,
        password=DB_PASSWORD,
        dbname='lb356'
    )
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE conversation_threads
            SET status = 'closed'
            WHERE thread_id = %s
        """, (thread_id,))

        conn.commit()
        print(f"[DB] Closed conversation thread: {thread_id}")
    except Exception as e:
        print(f"[DB ERROR] Failed to close conversation thread: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_conversation_status(thread_id):

    conn = get_connection(
        servername='sql1.njit.edu',
        username=DB_USERNAME,
        password=DB_PASSWORD,
        dbname='lb356'
    )
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT status
            FROM conversation_threads
            WHERE thread_id = %s
        """, (thread_id,))

        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"[DB ERROR] Failed to get conversation status: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def save_message_to_conversation(thread_id, chat_id, user_id, sender_role, message_text, telegram_message_id, source_email_id, timestamp):

    conn = get_connection(
        servername='sql1.njit.edu',
        username=DB_USERNAME,
        password=DB_PASSWORD,
        dbname='lb356'
    )
    
    cursor = conn.cursor()
    try:

        # Handle timestamp conversion - support both datetime objects and Telegram's datetime
        if hasattr(timestamp, 'strftime'):
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        elif hasattr(timestamp, 'isoformat'):
            # Handle Telegram's datetime objects
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp_str = str(timestamp)
        
        # Insert row into Table
        cursor.execute("""
            INSERT INTO conversation_threads (
                thread_id,
                chat_id,
                user_id,
                sender_role,
                message_text,
                timestamp,
                telegram_message_id,
                source_email_id   
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            thread_id,
            chat_id,
            user_id,
            sender_role,
            message_text,
            timestamp,
            telegram_message_id,
            source_email_id
        ))

        # Commit to DB
        conn.commit()
        print(f"[DB] Saved message to conversation {thread_id} - role: {sender_role}")
    except Exception as e:
        print(f"[DB ERROR] Failed to save message: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_thread_id_by_telegram_message_id(chat_id, telegram_message_id):

    conn = get_connection(
        servername='sql1.njit.edu',
        username=DB_USERNAME,
        password=DB_PASSWORD,
        dbname='lb356'
    )
    
    cursor = conn.cursor()
    try:
        # Querey the conversation_threads table
        cursor.execute("""
                SELECT thread_id
                FROM conversation_threads
                WHERE chat_id = %s
                    AND telegram_message_id = %s
                LIMIT 1 
        """, (chat_id, telegram_message_id))

        result = cursor.fetchone()

        if result:
            thread_id = result[0]
            print(f"[DB] Found thread_id: {thread_id} for message_id: {telegram_message_id}")
            return thread_id
        else:
            print(f"[DB] No thread_id found for message_id: {telegram_message_id}")
            return None
    except Exception as e:
        print(f"[DB ERROR] Failed to get thread_id: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_conversation_history(thread_id, limit=10):

    conn = get_connection(
        servername='sql1.njit.edu',
        username=DB_USERNAME,
        password=DB_PASSWORD,
        dbname='lb356'
    )
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
                SELECT sender_role, message_text, timestamp
                FROM conversation_threads
                WHERE thread_id = %s
                ORDER BY timestamp ASC
                LIMIT %s
        """, (thread_id, limit))

        results = cursor.fetchall()

        # Convert datetime objects to strings for JSON serialization
        for result in results:
            if isinstance(result['timestamp'], datetime):
                result['timestamp'] = result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        print(f"[DB] Loaded {len(results)} messages for thread_id: {thread_id}")
        return results
    except Exception as e:
        print(f"[DB ERROR] Failed to get thread history: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
