import pymongo
import json
from bson.objectid import ObjectId
#from models.courses_model import Course, Chapter
# Connect to MongoDB
client = pymongo.MongoClient()
db = client["kimo"]
courses_collection = db["courses"]

courses_collection.create_index([("name", pymongo.ASCENDING)])
courses_collection.create_index([("date", pymongo.DESCENDING)])
courses_collection.create_index([("total_ratings", pymongo.DESCENDING)])

# Open the JSON file and load the data into a list of Course objects
with open("courses.json", "r") as f:
    data = json.load(f)

courses = [course for course in data]

print(courses)

# Insert each course document into the collection
for course in courses:
    # Generate _id values for the course and chapter documents
    for chapter in course["chapters"]:
        chapter["_id"] = ObjectId()
        chapter["positive_rating"] = 0
        chapter["negative_rating"] = 0
    
    course["total_positive_ratings"] = 0
    course["total_negative_ratings"] = 0

    # Insert the course document into the collection
    courses_collection.insert_one(course)

    print(f"Inserted course {course}.")

print("Import complete!")