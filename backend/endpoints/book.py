from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from db.session import SessionLocal
from models.book import Book
from schemas.book import BookCreate, BookUpdate, BookOut
from core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/books", tags=["Books"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return email
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# -------------------------------
# CREATE
# -------------------------------
@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
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
    current_user: str = Depends(get_current_user)
):
    query = db.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    total = query.count()
    books = query.offset(skip).limit(limit).all()

    book_list = [BookOut.from_orm(b) for b in books]
    return {"total": total, "items": book_list}

# -------------------------------
# READ - Single book
# -------------------------------
@router.get("/{book_id}", response_model=BookOut)
def get_book(
    book_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookOut.from_orm(book)

# -------------------------------
# UPDATE
# -------------------------------
@router.put("/{book_id}", response_model=BookOut)
def update_book(
    book_id: int, 
    book_in: BookUpdate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
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
def delete_book(
    book_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}