import uvicorn

from escola_api.api.v1 import aluno_controller
from src.escola_api.api.v1 import curso_controller
from src.escola_api.app import app

app.include_router(curso_controller.router)
app.include_router(aluno_controller.router)



if __name__ == "__main__":
    uvicorn.run("main:app")
