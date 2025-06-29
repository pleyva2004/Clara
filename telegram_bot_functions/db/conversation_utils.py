from datetime import datetime
import json


# When Clara sends first message
def create_conversation_thread(conn, conversation_id, chat_id, source_email_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO conversation_threads (conversation_id, chat_id, source_email_id, status)
            VALUES (%s, %s, %s, 'open')
        """, (conversation_id, chat_id, source_email_id))

        conn.commit()
        print(f"[DB] Created new conversation thread: {conversation_id} (open)")
    except Exception as e:
        print(f"[DB ERROR] Failed to create conversation thread: {e}")
        conn.rollback()
    finally:
        cursor.close()


def close_conversation_thread(conn, conversation_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE conversation_threads
            SET status = 'closed'
            WHERE conversation_id = %s
        """, (conversation_id,))

        conn.commit()
        print(f"[DB] Closed conversation thread: {conversation_id}")
    except Exception as e:
        print(f"[DB ERROR] Failed to close conversation thread: {e}")
        conn.rollback()
    finally:
        cursor.close()


def get_conversation_status(conn, conversation_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT status
            FROM conversation_threads
            WHERE conversation_id = %s
        """, (conversation_id,))

        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"[DB ERROR] Failed to get conversation status: {e}")
        return None
    finally:
        cursor.close()


def save_message_to_conversation(conn, conversation_id, chat_id, user_id, sender_role, message_text, telegram_message_id, source_email_id, timestamp):
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
            INSERT INTO conversation_messages (
                conversation_id,
                chat_id,
                user_id,
                sender_role,
                message_text,
                timestamp,
                telegram_message_id,
                source_email_id   
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            conversation_id,
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
        print(f"[DB] Saved message to conversation {conversation_id} - role: {sender_role}")
    except Exception as e:
        print(f"[DB ERROR] Failed to save message: {e}")
        conn.rollback()
    finally:
        cursor.close()



def get_conversation_id_by_telegram_message_id(conn, chat_id, telegram_message_id):
    cursor = conn.cursor()
    try:
        # Querey the conversation_message table
        cursor.execute("""
                SELECT conversation_id
                FROM conversation_threads
                WHERE chat_id = %s
                    AND telegram_message_id = %s
                LIMIT 1 
        """, (chat_id, telegram_message_id))

        result = cursor.fetchone()

        if result:
            conversation_id = result[0]
            print(f"[DB] Found conversation_id: {conversation_id} for message_id: {telegram_message_id}")
            return conversation_id
        else:
            print(f"[DB] No conversation_id found for message_id: {telegram_message_id}")
            return None
    except Exception as e:
        print(f"[DB ERROR] Failed to get conversation_id: {e}")
        return None
    finally:
        cursor.close()

def get_conversation_history(conn, conversation_id, limit=10):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
                SELECT sender_role, message_text, timestamp
                FROM conversation_messages
                WHERE conversation_id = %s
                ORDER BY timestamp ASC
                LIMIT %s
        """, (conversation_id, limit))

        results = cursor.fetchall()

        # Convert datetime objects to strings for JSON serialization
        for result in results:
            if isinstance(result['timestamp'], datetime):
                result['timestamp'] = result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[DB] Loaded {len(results)} messages for conversation_id: {conversation_id}")
        return results
    except Exception as e:
        print(f"[DB ERROR] Failed to get conversation history: {e}")
        return []
    finally:
        cursor.close()
