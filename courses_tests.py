from fastapi.testclient import TestClient
from bson import ObjectId

from server import app
from configs.db import collection

client = TestClient(app)

def test_find_all_courses():
    response = client.get("/courses")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 4  # Assuming there are three courses in the database

def test_sort_courses():
    response = client.get("/courses?sort=title")
    assert response.status_code == 200
    assert response.json()["data"][0]["name"] < response.json()["data"][1]["name"]  # Assuming courses are sorted by name

def test_filter_courses():
    response = client.get("/courses?domain=artificial%20intelligence")
    assert response.status_code == 200
    for course in response.json()["data"]:
        assert "artificial intelligence" in course["domain"]    # Assuming all courses in the response have the specified domain

def test_get_course_overview():
    course_id = str(collection.find_one()["_id"])  # Assuming there is at least one course in the database
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    assert "name" in response.json()["data"]  # Assuming the course overview includes a "name" field

def test_get_chapter_info():
    course_id = str(collection.find_one()["_id"])  # Assuming there is at least one course in the database
    chapter_id = str(collection.find_one({"_id": ObjectId(course_id)})["chapters"][0]["_id"])  # Assuming the first course has at least one chapter
    response = client.get(f"/courses/{course_id}/chapters/{chapter_id}")
    assert response.status_code == 200
    assert "name" in response.json()["data"]  # Assuming the chapter information includes a "title" field

def test_rate_chapter():
    course_id = str(collection.find_one()["_id"])  # Assuming there is at least one course in the database
    chapter_id = str(collection.find_one({"_id": ObjectId(course_id)})["chapters"][0]["_id"])  # Assuming the first course has at least one chapter
    response = client.post(f"/courses/{course_id}/chapters/{chapter_id}/rate", json={"type": "positive"})
    assert response.status_code == 200
    chapter = collection.find_one({"_id": ObjectId(course_id)}, {"chapters": {"$elemMatch": {"_id": ObjectId(chapter_id)}}})["chapters"][0]
    assert chapter["positive_rating"] > 0  # Assuming the chapter's positive rating count was incremented by 1
    assert collection.find_one({"_id": ObjectId(course_id)})["total_positive_ratings"] > 0  # Assuming the course's total positive rating count was incremented by 1