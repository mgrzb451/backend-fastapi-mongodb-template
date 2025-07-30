from fastapi import APIRouter, Depends
from ..database.crud import students_crud
from ..database.models import StudentIn, StudentUpdate, Student
from ..database.db import mongo_cluster

# Instead of specifying "/students/" in every single path operation decorator we can add the prefix to the router and it will be present on every path operation.
# CAUTION: don't add a trailing / or they will be duplicated in the path operation e.g. here we'd have `/students/` and in the path operation another `/` and it would result in `/students//`
students_router = APIRouter(prefix="/students")

# WARNING: the word 'id' is a built-in function in python. Don't use it for variable names!

add_student_description = """# Add a new Student to the Database
Remember to include all the **fields**
## And don't cheat with the grades!
### Also _Markdown_
"""
@students_router.post("/", response_model=Student, status_code=201, description=add_student_description)
# We use Dependency injection function defined in the db.py module under mongo_cluster.get_students_collection(). It returns the async collection from mongo. The Dependency Injection mechanism will automatically pass the collection to the underlying CRUD method at an appropriate time
async def add_student(request: StudentIn, collection_injection=Depends(mongo_cluster.get_students_collection)):
  return await students_crud.add_student(request=request, collection=collection_injection)

@students_router.get("/", response_model=list[Student], summary="List all the students in the Database")
async def list_students(collection_injection=Depends(mongo_cluster.get_students_collection)):
  return await students_crud.get_all_students(collection=collection_injection)

@students_router.get("/{id}/", response_model=Student)
async def get_student(id:str, collection_injection=Depends(mongo_cluster.get_students_collection)):
  return await students_crud.get_student(id=id, collection=collection_injection)

@students_router.patch("/{id}/", response_model=Student)
async def update_student(id:str, request:StudentUpdate, collection_injection=Depends(mongo_cluster.get_students_collection)):
  return await students_crud.update_student(id=id, request=request, collection=collection_injection)

# We use 204 for response code. Means successful deletion, nothing to send back
@students_router.delete("/{id}/", status_code=204)
async def remove_student(id:str, collection_injection=Depends(mongo_cluster.get_students_collection)):
  await students_crud.delete_student(id=id, collection=collection_injection)