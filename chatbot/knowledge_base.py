import sqlite3
import os
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.db")

# NEW: Database initialization function
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS kb_responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 intent TEXT NOT NULL,
                 response TEXT NOT NULL)''')
    
    # Insert some sample data if table is empty
    c.execute("SELECT COUNT(*) FROM kb_responses")
    if c.fetchone()[0] == 0:
        sample_data = [
            ('greet', '👋 Hello! I\'m WellBot. How are you feeling today?'),
            ('greet', 'Hi there! 😊 I\'m doing well, thanks for asking. How about you?'),
            ('positive_mood', '😊 That\'s wonderful to hear! Keep spreading the good vibes!'),
            ('thanks', 'You\'re welcome! 💙'),
            ('goodbye', 'Goodbye! 👋 Take care of yourself.'),
        ]
        
        c.executemany("INSERT INTO kb_responses (intent, response) VALUES (?, ?)", sample_data)
    
    conn.commit()
    conn.close()

# Initialize the database when this module is imported
init_db()

# Rest of your existing functions...
def get_response_from_db(intent):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT response FROM kb_responses WHERE intent=?", (intent,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return None
    return random.choice([r[0] for r in rows])

def add_response(intent, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO kb_responses (intent, response) VALUES (?, ?)", (intent, response))
    conn.commit()
    conn.close()