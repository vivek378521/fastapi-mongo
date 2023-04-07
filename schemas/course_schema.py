from typing import List

def chapter_serializer(chapter) -> dict:
    return {
        'id': str(chapter["_id"]),
        'name': chapter["name"],
        'text': chapter["text"],
        'positive_rating': chapter["positive_rating"],
        'negative_rating': chapter["negative_rating"]
    }

def chapters_serializer(chapters: List[dict]) -> List[dict]:
    return [chapter_serializer(chapter) for chapter in chapters]

def course_serializer(course) -> dict:
    return {
        'id': str(course["_id"]),
        'name': course["name"],
        'date': course["date"],
        'description': course["description"],
        'domain': course["domain"],
        'chapters': chapters_serializer(course["chapters"]),
        'total_positive_ratings': course["total_positive_ratings"],
        'total_negative_ratings': course["total_negative_ratings"]
    }

def courses_serializer(courses: List[dict]) -> List[dict]:
    return [course_serializer(course) for course in courses]