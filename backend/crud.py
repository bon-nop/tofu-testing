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


def get_warehouse(db: Session, warehouse_id: int):
    return db.query(models.Warhouse).filter(models.Warhouse.id == warehouse_id).first()


def get_warehouses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Warhouse).offset(skip).limit(limit).all()


def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    db_warehouse = models.Warhouse(wh_name=warehouse.wh_name, door_1=warehouse.door_1, door_2=warehouse.door_2, 
                                   door_3=warehouse.door_3, door_4=warehouse.door_4, created_at=warehouse.created_at, 
                                   updated_at=warehouse.updated_at)
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


def update_warehouse(db: Session, update_data: schemas.WarehouseCreate, warehouse_id: int):
    db_warehouse = get_warehouse(db, warehouse_id)

    if db_warehouse is None:
        return None  # warehouse not found

    # Update warehouse attributes based on the data in update_data
    for key, value in update_data.dict().items():
        setattr(db_warehouse, key, value)

    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


def get_queue(db: Session, q_id: int):
    return db.query(models.Queue).filter(models.Queue.id == q_id).first()


def get_queues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Queue).offset(skip).limit(limit).all()


def create_queue(db: Session, queue: schemas.QueueCreate):
    db_queue = models.Queue(wh_id=queue.wh_id, door=queue.door, vehicle_types=queue.vehicle_types, vehicle_license=queue.vehicle_license,
                            start_load_time=queue.start_load_time, finish_load_time=queue.finish_load_time, status=queue.status,
                            created_at=queue.created_at, updated_at=queue.updated_at)
    db.add(db_queue)
    db.commit()
    db.refresh(db_queue)
    return db_queue


def update_queue(db: Session, update_data: schemas.QueueCreate, q_id: int):
    db_queue = get_queue(db, q_id)

    if db_queue is None:
        return None  # warehouse not found

    # Update warehouse attributes based on the data in update_data
    for key, value in update_data.dict().items():
        setattr(db_queue, key, value)

    db.commit()
    db.refresh(db_queue)
    return db_queue


def delete_queue(db: Session, q_id: int):
    db_queue = get_queue(db, q_id)
    db.delete(db_queue)
    db.commit()
    return db_queue
