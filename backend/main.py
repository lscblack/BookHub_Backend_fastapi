from fastapi import FastAPI
from db.session import Base, engine
from endpoints import auth, book


Base.metadata.create_all(bind=engine)


app = FastAPI(title="FastAPI JWT + Book CRUD")


app.include_router(auth.router)
app.include_router(book.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI JWT + Book Management"}