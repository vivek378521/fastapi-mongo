from typing import Optional
from fastapi import APIRouter, Query, HTTPException, Body
from models.courses_model import Course
from schemas.course_schema import courses_serializer, course_serializer, chapter_serializer
from bson import ObjectId
from configs.db import collection

course = APIRouter()

@course.get("/courses")
def find_all_courses(sort: Optional[str] = Query(
        None,
        title="Sort mode",
        description="The mode to sort the courses by",
        regex="^(title|date|p_rating|n_rating)$",
        example="title",
        choices=["title", "rating", "date"]
    ),
    domain: Optional[str] = Query(
        None,
        title="Course domain",
        description="The domain to filter the courses by",
        example="artificial intelligence",
    ),):
    # Define the sort key based on the requested sort mode
    if sort == "title":
        sort_key = [("name", 1)]
    elif sort == "date":
        sort_key = [("date", -1)]
    elif sort == "p_rating":
        sort_key = [("total_positive_ratings", -1)]
    elif sort == "n_rating":
        sort_key = [("total_negative_ratings", -1)]
    else:
        sort_key = []

    # Define the filter based on the requested domain
    if domain:
        filter_ = {"domain": domain}
    else:
        filter_ = {}

    # Query the collection with the sort key and filter
    courses = collection.find(filter=filter_, sort=sort_key)

    # Serialize the courses and return the response
    serialized_courses = courses_serializer(courses)
    return {"status": "Ok", "data": serialized_courses}

@course.get("/courses/{course_id}")
def get_course_overview(course_id: str):
    # Query the collection for the specified course ID
    course = collection.find_one({"_id": ObjectId(course_id)})

    # If the course is not found, return a 404 Not Found response
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return {"status": "Ok", "data": course_serializer(course)}

@course.get("/courses/{course_id}/chapters/{chapter_id}")
def get_chapter_info(course_id: str, chapter_id: str):
    # Query the collection for the specified course ID and chapter ID
    course = collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    chapter = next((x for x in course["chapters"] if str(x["_id"]) == chapter_id), None)

    # If the chapter is not found, return a 404 Not Found response
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Extract the chapter information from the chapter and return it in a JSON object
    return {"status": "Ok", "data": chapter_serializer(chapter)}

@course.post("/courses/{course_id}/chapters/{chapter_id}/rate")
def rate_chapter(course_id: str, chapter_id: str, rating: dict = Body(..., example={
    "type": "positive"
})):
    # Query the collection for the specified course ID and chapter ID
    course = collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    chapter = next((x for x in course["chapters"] if str(x["_id"]) == chapter_id), None)

    # If the chapter is not found, return a 404 Not Found response
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    rating_type = rating.get('type')
    if not rating_type or rating_type not in ['positive', 'negative']:
        raise HTTPException(status_code=400, detail="Invalid rating type")

    # Increment the chapter's positive/negative rating count
    if rating_type == "positive":
        chapter["positive_rating"] = chapter.get("positive_rating", 0) + 1
        course["total_positive_ratings"] = course.get("total_positive_ratings", 0) + 1
    elif rating_type == "negative":
        chapter["negative_rating"] = chapter.get("negative_rating", 0) + 1
        course["total_negative_ratings"] = course.get("total_negative_ratings", 0) + 1

    # Update the course and chapter data in the database
    collection.update_one({"_id": ObjectId(course_id)}, {"$set": course})

    # Return a success response
    return {"status": "Ok"}