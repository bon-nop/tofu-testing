# from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

import pandas as pd

import logging

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = logging.getLogger(__name__)

# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db, member=member)


@app.get("/members/", response_model=list[schemas.Member])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db, skip=skip, limit=limit)
    return members


@app.get("/members/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@app.put("/members/{member_id}", response_model=schemas.Member)
def update_member(member_id: int, update_data: schemas.MemberCreate, db: Session = Depends(get_db)):
    updated_member = crud.update_member(db, update_data, member_id)

    if updated_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return updated_member
    

@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    crud.delete_member(db, member_id)
    return {"message": "Member deleted"}


@app.get("/export")
def export_members_excel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    excel_file_path = crud.get_members_as_excel(db, skip, limit)

    # Open the Excel file for binary reading
    with open(excel_file_path, "rb") as file:
        file_contents = file.read()

    # Return the Excel file as a response
    response = Response(content=file_contents)
    response.headers["Content-Disposition"] = f'attachment; filename="members.xlsx"'
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response


@app.get("/export/{member_id}")
def export_member_excel(member_id: int, db: Session = Depends(get_db)):
    excel_file_path = crud.get_member_as_excel(db, member_id)

    if not excel_file_path:
        raise HTTPException(status_code=404, detail="Member not found")

    # Open the Excel file for binary reading
    with open(excel_file_path, "rb") as file:
        file_contents = file.read()

    # Return the Excel file as a response
    response = Response(content=file_contents)
    response.headers["Content-Disposition"] = f'attachment; filename="member_{member_id}.xlsx"'
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response