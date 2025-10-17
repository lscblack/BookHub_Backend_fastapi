from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from db.session import SessionLocal
from models.book import Book
from schemas.book import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/books", tags=["Books"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# CREATE
# -------------------------------
@router.post("/", response_model=BookOut)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    book = Book(**book_in.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return BookOut.from_orm(book)


# -------------------------------
# READ - List with pagination & filters
# -------------------------------
@router.get("/", response_model=dict)
def list_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(10, le=100),
    title: Optional[str] = None,
    author: Optional[str] = None,
):
    query = db.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    total = query.count()
    books = query.offset(skip).limit(limit).all()

    # Convert SQLAlchemy models → Pydantic
    book_list = [BookOut.from_orm(b) for b in books]

    return {"total": total, "items": book_list}


# -------------------------------
# READ - Single book
# -------------------------------
@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookOut.from_orm(book)


# -------------------------------
# UPDATE
# -------------------------------
@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_in.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return BookOut.from_orm(book)


# -------------------------------
# DELETE
# -------------------------------
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
