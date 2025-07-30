from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

'''Remember that unlike with SQL we're using these models for both request and response data validation. Gotta think which model will be applicable in each scenario. E.g. Student class we use in a response so we'll get an "_id" in the ObjectId format from Mongo - that's why we have to use the `Annotated[str, BeforeValidator(str)]` construct to convert it into a string first
But in the case of StudentUpdate which we use to validate the request we will get the id from the frontend in the form of a string, so we don't have to convert into a string. Just a small optimization 😉'''

class StudentIn(BaseModel):
  name: str = Field(min_length=2)
  email: str = Field(min_length=3) # there is an EmailStr class that can be used to validate emails
  grades_avg: float = Field(le=6) # required attribute of type float that has to be <=6
  courses: list[str] = Field(min_length=1) # require a list of string with at least 1 item
  model_config = ConfigDict(
    json_schema_extra={
      "example": {
          "name": "John Smith",
          "email": "js@mail.com",
          "courses": ["math", "pe", "english"],
          "grades_avg": 3.0
      }
    }
  )

class Student(StudentIn):
  # BeforeValidator is a construct that allows applying a function to the attribute (they call it field) before validation happens. Here we're converting the ObjectId from Mongo into a normal string before pydantic validates the data. This conversion is an actual conversion. The id will be of type string afterwards, not just for the duration of the validation process
  id: Annotated[str, BeforeValidator(str)] = Field(alias="_id")
  model_config = ConfigDict(
    # arbitrary_types_allowed=True mongo uses its custom ObjectId type for the "_id" we have to let pydantic know it's ok to use it
    arbitrary_types_allowed=True,
    # mongo uses "_id" for the name but we ERRONEOUSLY used "id" (that's not good cause it shadows pythons' built-in function name Ooops, should've used student_id or smth) so we need to let Pydantic know to fill in the "id" field with "_id" or vice versa 
    populate_by_name=True
  )

class StudentUpdate(BaseModel):
  # Field(default, rest of arg)
  # so here we're saying name is optional by specifying name: str|None = None
  # but then we're adding that if you do provide a string as a name it has to >= 2 chars
  name: str | None = Field(None, min_length=2)
  # The above is the same as this one using Annotated. We're saying name has to be str or None; defaults to None so it's optional; and then if provided it has to >=2 chars long
  # name: Annotated[str | None, Field(None, min_length=2)]
  email: str | None = Field(None, min_length=2)
  grades_avg: float | None = Field(None, le=6)
  # an optional list of strings. The default is None so it's optional. And then if it's supplied it has to be of length 1 minimum
  courses: Annotated[list[str] | None, Field(default=None, min_length=1)]
  model_config = ConfigDict(
    arbitrary_types_allowed=True,
    populate_by_name=True 
  )

  