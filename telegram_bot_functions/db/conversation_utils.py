from datetime import datetime

def save_message_to_conversation(conn, conversation_id, chat_id, user_id, sender_role, message_text, telegram_message_id, source_email_id, timestamp):
    cursor = conn.cursor()

    # Ensure time is in MySQL format
    if isinstance(timestamp, datetime):
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
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

def get_conversation_id_by_telegram_message_id(conn, chat_id, telegram_message_id):
    cursor = conn.cursor()

    # Querey the conversation_message table
    cursor.execute("""
            SELECT conversation_id
            FROM conversation_messages
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

def get_conversation_history(conn, conversation_id, limit=10):
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
            SELECT sender_role, message_text, timestamp
            FROM conversation_messages
            WHERE conversation_id = %s
            ORDER BY timestamp ASC
            LIMIT %s
    """, (conversation_id, limit))

    results = cursor.fetchall()

    print(f"[DB] Loaded {len(results)} messages for conversation_id: {conversation_id}")

    return results