from fastapi import FastAPI
from .routes.file_routes import router as file_router
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow specific HTTP methods
    allow_headers=["*"],  
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the file upload router
app.include_router(file_router)
