from fastapi import FastAPI
from routes import users, tasks, category
import uvicorn

app = FastAPI()
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(category.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
