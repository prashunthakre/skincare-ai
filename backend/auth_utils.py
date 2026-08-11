import sqlite3
import hashlib
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            dob TEXT,
            password_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, phone, dob, email, password):
    email = email.lower().strip()
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Check if user already exists
        c.execute("SELECT email FROM users WHERE email = ?", (email,))
        if c.fetchone():
            conn.close()
            return False, "This email is already registered."
            
        # Insert user
        c.execute(
            "INSERT INTO users (email, name, phone, dob, password_hash) VALUES (?, ?, ?, ?, ?)",
            (email, name, phone, str(dob), hash_password(password))
        )
        conn.commit()
        conn.close()
        return True, "Registration successful! You can now log in."
        
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def login_user(email, password):
    email = email.lower().strip()
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        c.execute("SELECT name, password_hash FROM users WHERE email = ?", (email,))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return False, "This mail id is not registered with us."
            
        name, stored_hash = row
        
        if stored_hash == hash_password(password):
            return True, name
        else:
            return False, "Incorrect password."
            
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
