# security/security.py

import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL not found in .env")

def get_db_connection():
    try:
        print("[DB] Connecting to PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        print("[DB] Connected.")
        return conn
    except Exception as e:
        print(f"[DB ERROR] Connection failed: {e}")
        raise

def save_session(user_id: int, session: dict):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        print(f"[DB] Saving session for user_id: {user_id}")

        cur.execute("""
            INSERT INTO user_sessions (
                user_id, clientcode, access_token, refresh_token,
                feed_token, state, profile_json
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET
                clientcode = EXCLUDED.clientcode,
                access_token = EXCLUDED.access_token,
                refresh_token = EXCLUDED.refresh_token,
                feed_token = EXCLUDED.feed_token,
                state = EXCLUDED.state,
                profile_json = EXCLUDED.profile_json;
        """, (
            user_id,
            session["clientcode"],
            session["access_token"],
            session["refresh_token"],
            session["feed_token"],
            session["state"],
            json.dumps(session.get("profile", {}))
        ))

        conn.commit()
        print(f"[DB] Session saved and committed.")
    except Exception as e:
        print(f"[DB ERROR] Failed to save session: {e}")
    finally:
        cur.close()
        conn.close()

def get_session(user_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT clientcode, access_token, refresh_token, feed_token, state, profile_json
            FROM user_sessions WHERE user_id = %s
        """, (user_id,))
        row = cur.fetchone()

        if row:
            print(f"[DB] Session found for user_id {user_id}")
            return {
                "clientcode": row[0],
                "access_token": row[1],
                "refresh_token": row[2],
                "feed_token": row[3],
                "state": row[4],
                "profile": json.loads(row[5]) if isinstance(row[5], str) else row[5]
            }
        else:
            print(f"[DB] No session found for user_id {user_id}")
            return None
    except Exception as e:
        print(f"[DB ERROR] Failed to fetch session: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def is_logged_in(user_id: int):
    session = get_session(user_id)
    is_active = session is not None
    print(f"[DB] is_logged_in({user_id}) = {is_active}")
    return is_active


