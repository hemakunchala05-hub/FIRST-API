from typing import Optional

from fastapi import FastAPI,Depends
from pydantic import BaseModel  

from sqlalchemy.orm import Session

from conn import get_db,engine
import db
from db import Notes,User





models = db.Base.metadata.create_all(bind=engine)



app = FastAPI()
class Note(BaseModel):
    id: int
    title: str
    content: str
    user_id: Optional[int] = None

@app.get("/notes/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
    note = db.query(Notes).filter(Notes.id == id).first()
    if note:
        return note
    else:
        return {"error": "Note not found"}
    
@app.post("/notes")
def create_note(note: Note, db: Session = Depends(get_db)):
    db_note = Notes(
        id=note.id,
        title=note.title,
        content=note.content,
        user_id=note.user_id,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {"message": "Note created successfully"}

@app.get("/notes")
def get_all_notes(db: Session = Depends(get_db)):
    return db.query(Notes).all()

@app.put("/notes/{id}")
def update_note(id: int, note: Note, db: Session = Depends(get_db)):
    db_note = db.query(Notes).filter(Notes.id == id).first()
    if db_note:
        db_note.content = note.content
        db_note.title = note.title
        db.commit()
        db.refresh(db_note)
        return {"message": "Note updated successfully"}
    else:
        return {"error": "Note not found"}
    
@app.delete("/notes/{id}")
def delete_note(id: int, db: Session = Depends(get_db)):
    db_note = db.query(Notes).filter(Notes.id == id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return {"message": "Note deleted successfully"}
    else:
        return {"error": "Note not found"}

 

