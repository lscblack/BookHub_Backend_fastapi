from fastapi import FastAPI
from db.session import engine, Base
from endpoints import auth


# create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="FastAPI JWT Auth (SQLite)")


app.include_router(auth.router)


# root
@app.get("/")
def root():
    return {"message": "FastAPI JWT Auth — visit /docs for Swagger UI"}