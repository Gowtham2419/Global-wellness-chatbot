import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('wellness_chatbot.db')

# View users table
print("=== USERS TABLE ===")
users_df = pd.read_sql_query("SELECT * FROM users", conn)
print(users_df)

print("\n=== CONVERSATIONS TABLE ===")
# View conversations table
conv_df = pd.read_sql_query("SELECT * FROM conversations", conn)
print(conv_df)

conn.close()