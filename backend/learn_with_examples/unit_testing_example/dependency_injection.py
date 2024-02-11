from fastapi import FastAPI, Depends, HTTPException, status

development_db = ["DB for Development"]


def get_db_session():
    return development_db


app = FastAPI()


@app.post("/items")
def add_item(item: str, db = Depends(get_db_session)):
    db.append(item)
    print(db)
    return {"message":f"added item {item}"}