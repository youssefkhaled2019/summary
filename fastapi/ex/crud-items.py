# ====================== core/database.py ======================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"
#DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()
# ====================== core/dependencies.py ======================

from core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ====================== item/model.py ======================
from sqlalchemy import Column, Integer, String
from core.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
# ====================== item/schema.py ======================
from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    title: str
    description: str


class ItemResponse(BaseModel):
    id: int
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
# ====================== item/router.py ======================
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from item.model import Item
from item.schema import ItemCreate, ItemResponse,ItemUpdate
from core.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    new_item = Item(
        title=item.title,
        description=item.description
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@router.get("/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):

    items = db.query(Item).all()

    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()

    return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    data: ItemCreate,
    db: Session = Depends(get_db)
):

    item = db.query(Item).filter(Item.id == item_id).first()

    item.title = data.title
    item.description = data.description

    db.commit()
    db.refresh(item)

    return item

@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}


# ====================== main.py ======================
from fastapi import FastAPI
from core.database import engine, Base
from item.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

app.include_router(router, prefix="/items")
# ====================== test/ ======================




# ====================== api/ ======================
# {
#   "title": "Laptop",
#   "description": "Gaming laptop"
# }