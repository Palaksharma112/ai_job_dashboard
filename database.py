import sqlite3
import bcrypt

DB_NAME = "users.db"


# ==========================================
# Database Connection
# ==========================================

def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================
# Create Users Table
# ==========================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            fullname TEXT NOT NULL,

            email TEXT NOT NULL,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# Register User
# ==========================================

def register_user(fullname, email, username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username=?",
        (username,)
    )

    if cursor.fetchone():
        conn.close()
        return False

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        INSERT INTO users
        (fullname,email,username,password)

        VALUES(?,?,?,?)
        """,
        (
            fullname,
            email,
            username,
            hashed
        )
    )

    conn.commit()
    conn.close()

    return True


# ==========================================
# Login User
# ==========================================

def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return False

    stored_password = row[0]

    return bcrypt.checkpw(
        password.encode(),
        stored_password.encode()
    )


# ==========================================
# Get User
# ==========================================

def get_user(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        fullname,
        email,
        username

        FROM users

        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ==========================================
# Update Profile
# ==========================================

def update_profile(fullname, email, username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users

        SET
        fullname=?,
        email=?

        WHERE username=?
        """,
        (
            fullname,
            email,
            username
        )
    )

    conn.commit()
    conn.close()


# ==========================================
# Change Password
# ==========================================

def change_password(username, new_password):

    hashed = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    ).decode()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users

        SET password=?

        WHERE username=?
        """,
        (
            hashed,
            username
        )
    )

    conn.commit()
    conn.close()


# ==========================================
# Delete User (Optional)
# ==========================================

def delete_user(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()
    conn.close()


# ==========================================
# Total Users
# ==========================================

def total_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count