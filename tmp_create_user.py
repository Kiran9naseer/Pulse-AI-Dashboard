from database.db import init_db, create_user

init_db()
if create_user("test@pulse.ai", "password123"):
    print("User created successfully!")
else:
    print("User already exists or failed to create.")
