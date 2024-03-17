from fastapi import  APIRouter, FastAPI, Depends, HTTPException, status, Response

from  database import engine,SessionLocal, Base
from schema import UserSchema
from sqlalchemy.orm import Session
from models import User

#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/users")   

def get_db():
    try:
        db = SessionLocal()
        #TODO 
        yield db
    finally:
        db.close()

@router.post("/add")
async def add_produto(request:UserSchema, db: Session = Depends(get_db)):
    user_no_db = User(id=request.id, username=request.username, password=request.password)
    db.add(user_no_db)
    db.commit()
    db.refresh(user_no_db)
    return user_no_db

@router.get("/{user_name}", description="Buscar usuário pelo nome")
def get_produtos(user_name,db: Session = Depends(get_db)):
    user_no_db= db.query(User).filter(User.username == user_name).first()
    return user_no_db

@router.get("/users/listar")
async def get_tarefas(db: Session = Depends(get_db)):
    users= db.query(User).all()
    return users


@router.delete("/{id}", description="Deletar o usuário pelo id")
def delete_produto(id: int, db: Session = Depends(get_db)):
    user_no_db = db.query(User).filter(User.id == id).first()
    if user_no_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sem usuário com este id')
    db.delete(user_no_db)
    db.commit()
    return f"Banco com id {id} deletado.", Response(status_code=status.HTTP_200_OK)