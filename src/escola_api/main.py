from calendar import month
from dataclasses import dataclass, field
from datetime import datetime, date

import uvicorn
from dataclasses_json import dataclass_json, LetterCase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def index():
    return {"mensagem": "Olá Mundo"}


@app.get("/calculadora")
def calculadora(numero1 : int, numero2 : int):
    soma = numero1 + numero2
    return {"soma": soma}


@app.get("/processar-cliente")
def processar_cliente(nome: str, idade: int, sobrenome: str):
    nome_completo = nome + " " + sobrenome
    ano_nascimento = datetime.now().year - idade

    if ano_nascimento >= 1990 and ano_nascimento < 2000:
       decada = "decada de 90"
    elif ano_nascimento >= 1980 and ano_nascimento < 1990:
       decada = "decada de 80"
    elif ano_nascimento >= 1970 and ano_nascimento < 1980:
      decada = "decada de 70"
    else:
     decada = "decada abaixo de 70 ou acima de 90"

    return {
        "nome": nome_completo,
        "ano_nascimento": ano_nascimento,
        "decada:": decada,
    }

@dataclass
class Curso:
    id: int = field()
    nome: str = field()
    sigla: str = field()

@dataclass
class CursoCadastro:
    nome: str = field()
    sigla: str = field()

@dataclass
class CursoEditar:
    nome: str = field()
    sigla: str = field()

cursos = [
    # instanciando um objeto da classe Curso
    Curso( id = 1, nome = "Python Web", sigla = "PY1"),
    Curso(id = 2, nome= "Git e GitHub", sigla="GT")
]

@app.get("/api/cursos")
def listar_todos_cursos():
    return  cursos

@app.get("/api/cursos/{id}")
def obter_por_id_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            return curso

    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")

@app.post("/api/cursos")
def cadastrar_curso(form: CursoCadastro):
    ultimo_id = max([curso.id for curso in cursos], default=0)

    curso = Curso(id = ultimo_id + 1, nome=form.nome, sigla=form.sigla)

    cursos.append(curso)

    return curso

@app.delete("/api/cursos/{id}", status_code=204)
def apagar_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            cursos.remove(curso)
            return
    raise HTTPException(status_code=404, detail=f"curso não encontrado com id : {id}")


@app.put("/api/cursos/{id}")
def editar_curso(id: int, form: CursoEditar):
    for curso in cursos:
        if curso.id == id:
            curso.nome = form.nome
            curso.sigla = form.sigla
            return curso
    raise HTTPException(status_code=404, detail=f"curso não encontrado com id : {id}")



## AREA ALUNOS

class Aluno(BaseModel):
    id: int = field()
    nome: str = field()
    sobrenome: str = field()
    cpf: str = field()
    data_nascimento: datetime = Field(alias="dataNascimento")



class AlunoCadastro(BaseModel):
    nome: str = field()
    sobrenome: str = field()
    cpf: str = field()
    data_nascimento: datetime = Field(alias="dataNascimento")



class AlunoEditar(BaseModel):
    nome: str = field()
    sobrenome: str = field()
    cpf: str = field()
    data_nascimento: datetime = Field(alias="dataNascimento")

alunos = [
    # instanciando um objeto da classe Curso
    Aluno( id = 1, nome = "Rhamon", sobrenome= "Almeida", cpf="161.074.517-57", dataNascimento = date(1996,4,23)),
    Aluno(id=2, nome="Larissa", sobrenome="Menezes", cpf="432.781.229-30", dataNascimento = date(1999,10,18)),
    Aluno(id=3, nome="Carlos", sobrenome="Souza", cpf="205.467.880-92", dataNascimento = date(2006,4,12)),
]

@app.get("/api/alunos")
def listar_todos_alunos():
    return alunos

@app.get("/api/alunos/{id}")
def obter_aluno(id: int):
    for aluno in alunos:
        if aluno.id == id:
            return aluno
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@app.post("/api/alunos")
def cadastrar_aluno(form: AlunoCadastro):
    ultimo_id = max([aluno.id for aluno in alunos], default=0)

    aluno = Aluno(id = ultimo_id + 1, nome=form.nome, sobrenome= form.sobrenome, cpf=form.cpf, data_nascimento = form.data_nascimento)

    alunos.append(aluno)
    return aluno

@app.put("/api/alunos/{id}")
def editar_aluno(id: int, form: AlunoEditar):
    for aluno in alunos:
        if aluno.id == id:
            aluno.nome = form.nome
            aluno.sobrenome = form.sobrenome
            aluno.cpf = form.cpf
            aluno.data_nascimento = form.data_nascimento
            return aluno
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id : {id}")

@app.delete("/api/alunos/{id}")
def apagar_aluno(id: int):
    for aluno in alunos:
        if aluno.id == id:
            alunos.remove(aluno)
            return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id : {id}")


if __name__ == "__main__":
    uvicorn.run("main:app")
