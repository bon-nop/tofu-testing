from sqlalchemy.orm import Session

from . import models, schemas
import pandas as pd


def get_members_as_excel(db: Session, skip: int = 0, limit: int = 100):
    
    members = db.query(models.Member).offset(skip).limit(limit).all()
    member_data = [{"ไอดี": member.id, "ชื่อจริง": member.first_name, "นามสกุล": member.last_name,
                    "ตำแหน่ง": member.position, "ที่อยู่": member.address, "เงินเดือนที่คาดหวัง": member.expect_salary} for member in members]
    df = pd.DataFrame(member_data)

    # Specify the file path where you want to save the Excel file
    excel_file_path = "members.xlsx"

    # Save the DataFrame to an Excel file (xlsx format)
    df.to_excel(excel_file_path, index=False, sheet_name="Members")

    return excel_file_path  # Return the file path for later use


def get_member_as_excel(db: Session, member_id: int):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    
    if not member:
        return None  # Member not found

    member_data = [{"ไอดี": member.id, "ชื่อจริง": member.first_name, "นามสกุล": member.last_name,
                    "ตำแหน่ง": member.position, "ที่อยู่": member.address, "เงินเดือนที่คาดหวัง": member.expect_salary}]
    df = pd.DataFrame(member_data)

    # Specify the file path where you want to save the Excel file
    excel_file_path = f"member_{member_id}.xlsx"

    # Save the DataFrame to an Excel file (xlsx format)
    df.to_excel(excel_file_path, index=False, sheet_name="Member")

    return excel_file_path


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()


def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(first_name=member.first_name, last_name=member.last_name, 
                              position=member.position, address=member.address, expect_salary=member.expect_salary)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def update_member(db: Session, update_data: schemas.MemberCreate, member_id: int):
    db_member = get_member(db, member_id)

    if db_member is None:
        return None  # Member not found

    # Update member attributes based on the data in update_data
    for key, value in update_data.dict().items():
        setattr(db_member, key, value)

    db.commit()
    db.refresh(db_member)
    return db_member


def delete_member(db: Session, member_id: int):
    db_member = get_member(db, member_id)
    db.delete(db_member)
    db.commit()
    return db_member


# def create_member(db: Session, member: schemas.MemberCreate):
#     db_member = models.Member(first_name=member.first_name, last_name=member.last_name, 
#                               position=member.position, address=member.address, expect_salary=member.expect_salary)
#     db.add(db_member)
#     db.commit()
#     db.refresh(db_member)
#     return db_member