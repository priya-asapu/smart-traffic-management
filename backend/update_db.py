from sqlalchemy import text
from database import engine

with engine.begin() as connection:
    connection.execute(
        text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'user'")
    )

print("role column added")