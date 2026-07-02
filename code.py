from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel

from conn import get_db, engine
import db
from db import Notes, User
from auth import create_access_token, verify_password, get_current_user, auth_router













models = db.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(auth_router)

class Note(BaseModel):
    id: int
    title: str
    content: str
    user_id: Optional[int] = None

@app.get("/notes/{id}")
def get_note(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Notes).filter(Notes.id == id, Notes.user_id == current_user.id).first()
    if note:
        return note
    else:
        return {"error": "Note not found"}
    
@app.post("/notes")
def create_note(note: Note, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = Notes(
        id=note.id,
        title=note.title,
        content=note.content,
        user_id=current_user.id,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {"message": "Note created successfully"}

@app.get("/notes")
def get_all_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Notes).filter(Notes.user_id == current_user.id).all()

@app.put("/notes/{id}")
def update_note(id: int, note: Note, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(Notes).filter(Notes.id == id, Notes.user_id == current_user.id).first()
    if db_note:
        db_note.content = note.content
        db_note.title = note.title
        db.commit()
        db.refresh(db_note)
        return {"message": "Note updated successfully"}
    else:
        return {"error": "Note not found"}
    
@app.delete("/notes/{id}")
def delete_note(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(Notes).filter(Notes.id == id, Notes.user_id == current_user.id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return {"message": "Note deleted successfully"}
    else:
        return {"error": "Note not found"}

 

