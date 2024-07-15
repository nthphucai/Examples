import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.operations import (
    Item,
    ItemCreate,
    ItemUpdate,
    NotFoundError,
    create_db_item,
    delete_db_item,
    read_db_item,
    update_db_item,
)
from database.core import Base, DATABASE_URL

app = FastAPI()

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    return create_db_item(item, db)


@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        return read_db_item(item_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)) -> Item:
    try:
        return update_db_item(item_id, item, db)

    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        return delete_db_item(item_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    # In production, don't forget to change reload => False, debug => False
    uvicorn.run("run_db:app", host="0.0.0.0", port=int(5050), reload=True)
