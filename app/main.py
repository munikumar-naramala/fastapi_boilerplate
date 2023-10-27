from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.admin import admin_router
from app.api.endpoints.user import user_router
from app.api.endpoints.task import task_router
import uvicorn


app = FastAPI(
    title="INTERNS MANAGEMENT",
    version="1.0.0",
    openapi_url="/custom-openapi.json",
)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the routes
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(task_router, tags=['Admin Task Management'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)








