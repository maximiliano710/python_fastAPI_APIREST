#API REST: interfaz de programacion de aplicaciones para compatir recursos

from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# inicializamos una variabke en donde tendra todas las caracteristicas de una API REST
app = FastAPI()

class Curso(BaseModel):
    id:Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

#simularemos una base de datos

cursos_db = []

# CRUD: read (lectura) GET ALL: leeremos todos los cursos que haya en base de datos en la db

@app.get("/cursos/",response_model=list[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) POST: agregaremos un nuevo recurso a nuestra base de datos
@app.post("/cursos/",response_model=(Curso))
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) #usamos UUID para generar un id unico e irrepetible
    cursos_db.append(curso)
    return curso
    
# CRUD: Read (lectura) GET (individual): Leeremos el curso que coincida con el ID quepidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None)# con next tomamos la primera conincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail="Curso no encontrado")
    return curso

#CRUD_ Update (Actualizar/Modificar) PUT: modificaremos un curso que coincida con el ID que mandamos
@app.put("/cursos/{curso_id}",response_model=Curso)
def actualizar_curso(curso_id:str,curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso)# Buscamos el indice exacto dond esta el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD: Delete (Borrado/baja) DELETE: eliminaremos un recurso que coincida con el ID que mandamos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None)# con next tomamos la primera conincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404,detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
