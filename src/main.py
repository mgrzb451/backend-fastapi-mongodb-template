from fastapi import FastAPI
from src.database.db import lifespan
from src.routers.students_router import students_router

  
app = FastAPI(
  # lifespan function that will manage connecting to the mongodb cluster and creating a connection pool on application startup. It uses fastapis' mechanism for automatically calling subsequent parts of the function at the start of the app and after shutdown
  lifespan=lifespan,
  title="MongoDB+FastAPI Learning Project",
  description="Looking for best practices for FastAPI with PyMongo async operations"
)

# Even though we're using a router (like blueprints in Flask) for the main path operations we can still add a simple @app route. Here we have one for the home page
@app.get("/", response_model=dict[str,str])
async def home():
  return {"message": "Test Connection"}

# Add path operations defined in the students_router to the app. There are many ways to customize these. E.g. adding a common endpoint prefix like /school, specifying common tags, adding a dependency injection for all path operations and more
app.include_router(students_router)