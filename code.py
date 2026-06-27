from fastapi import FastAPI
from pydantic import BaseModel  

notes_dict= {}



app = FastAPI()
class Note(BaseModel):
    id : int
    title : str
    content : str  

@app.get("/notes/{id}")
def get_note(id: int):
    if id in notes_dict:
        return notes_dict[id]
    else:
        return {"error": "Note not found"}
    
@app.post("/notes")
def create_note(note: Note):
    notes_dict[note.id] = note
    return {"message": "Note created successfully"} 

@app.get("/notes")
def get_all_notes():
    return notes_dict

@app.put("/notes/{id}")
def update_note(id: int, note: Note):
    if id in notes_dict:
        notes_dict[id].content = note.content
        notes_dict[id].title = note.title
        return {"message": "Note updated successfully"}
    else:
        return {"error": "Note not found"}
    
@app.delete("/notes/{id}")
def delete_note(id: int):
    if id in notes_dict:
        del notes_dict[id]
        return {"message": "Note deleted successfully"}
    else:
        return {"error": "Note not found"}  


 

