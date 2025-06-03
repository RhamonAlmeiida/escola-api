import uvicorn

from escola_api.api.v1 import aluno_controller
from escola_api.database.banco_dados import engine, Base
from src.escola_api.api.v1 import curso_controller
from src.escola_api.app import app

app.include_router(curso_controller.router)
app.include_router(aluno_controller.router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app")
