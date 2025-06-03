from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

router = APIRouter()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # POST, GET, PUT, DELETE, PATCH, OPTIONS, HEAD
    allow_headers=["*"]
)
