import uvicorn

if __name__ == "__main__":
  uvicorn.run(app="src.main:app", reload=True)