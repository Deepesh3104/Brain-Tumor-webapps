from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import pymongo
import warnings
from motor.motor_asyncio import AsyncIOMotorClient

# Connection string for MongoDB Atlas
connection_string = "mongodb+srv://Deepesh2104:Deepesh2228@cluster0.7mgj9te.mongodb.net/deepesh?retryWrites=true&w=majority"

# Function to establish connection to MongoDB Atlas and return the collection
def connect_to_database():
    try:
        # Connect to MongoDB Atlas
        client = pymongo.MongoClient(connection_string)
        db = client["deepesh"]
        collection = db["user"] 
        return collection
    except pymongo.errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB Atlas. Error:", e)

# Function to insert a new user into the database
def insert_user(firstname, lastname, email, password):
    try:
        collection = connect_to_database()
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": hashed_password,
        }
        collection.insert_one(user_data)
        return True
    except Exception as e:
        print("Error inserting user:", e)
        return False

# Function to find a user by email in the database
def find_user_by_email(email):
    try:
        collection = connect_to_database()
        user = collection.find_one({"email": email})
        return user
    except Exception as e:
        print("Error finding user by email:", e)
        return None

# Function to authenticate a user by email and password
def authenticate_user(email, password):
    try:
        user = find_user_by_email(email)
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return user
        else:
            return None
    except Exception as e:
        print("Error authenticating user:", e)
        return None

if __name__ == "__main__":
    # Test database operations
    print("Testing database operations...")
    # Example usage: insert a new user
    if insert_user("John", "Doe", "john@example.com", "password123"):
        print("User inserted successfully!")
    else:
        print("Failed to insert user.")
