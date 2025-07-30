from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient


# Load parts of the URL from .env and dynamically construct the full URL with placeholder values of "<user_name>" & "<db_password>" filled in
load_dotenv()
mongo_url = os.getenv("mongo_url")
user = os.getenv("mongo_user")
password = os.getenv("mongo_password")
MONGODB_URL = mongo_url.replace("<user_name>", user).replace("<db_password>", password)

# Database and collection names
class MongoCluster:
  # The DB_NAME, COLLECTION_NAME, DB_URL and the process of loading them in from dotenv could probably be included here as well
  # Actually the RECOMMENDED approach to do these things is to use the pydantic BaseSettings class but I haven't explored that yet
  '''
  Class for storing Mongo Database and Collections in a neat and organized way
  It exposes methods used to connect to the database and methods for dependency injections in path operations
  '''

  # Class attributes with names of Mongo Database and collection
  DB_NAME="school"
  COLLECTION_NAME="students"

  # A placeholder class attribute of type AsyncMongoClient that we wil fill on class instantiation
  client: AsyncMongoClient

  async def test_connection(self):
    """
    Using the AsyncMongoClients' command() method to test the connection
    """
    await self.client["admin"].command("ping")

  async def get_school_db(self):
    """
    This is an unused method if we wanted to returns the entire database to perform some db level operations or use it in a dependency injection
    """
    return self.client.get_database(self.DB_NAME)
  
  async def get_students_collection(self):
    """
    This function returns the students collection. We need to access the collection for every path operation that performs CRUD. We will use fastapi trick of dependency injection with this function
    """
    return self.client.get_database(self.DB_NAME).get_collection(self.COLLECTION_NAME)
    
mongo_cluster = MongoCluster()

@asynccontextmanager
# even though app is not directly used in this function it's necessary for the lifetime parameter in the FastApi app to work
async def lifespan(app):
  """Connect to mongo and establish a connection pool"""
  mongo_cluster.client = AsyncMongoClient(MONGODB_URL)
  try:
    # test connection to cluster
    await mongo_cluster.test_connection()
    print("✅ Connected to MongoDB cluster")
  except Exception as error:
    raise RuntimeError(f"❌ Failed to connect to MongoDB: {error}")
  # all the code until yield will run on FastApi app startup. Then it will stop and the app can operate normally
  yield
  # When the server/fastapi app start to terminate the code after yield will start running
  # Close connection after app terminates
  await mongo_cluster.client.close()
  print("⏹ Closing connection to cluster")

