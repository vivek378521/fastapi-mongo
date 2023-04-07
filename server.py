from fastapi import FastAPI
app = FastAPI()

from routes.courses_routes import course
app.include_router(course)