from fastapi import FastAPI

from app.routers import items, reservations

app = FastAPI(title="GearShare API", version="0.1.0")
app.include_router(items.router)
app.include_router(reservations.router)


@app.get("/health", tags=["monitoring"])
def health():
    return {"status": "tout est bon"}

""""
from fastapi import Path
@app.get("/items/{item_id}")
def get_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}
from fastapi import Query

@app.get("/items")
def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
    disponible: bool | None = None,
):
    return {"skip": skip, "limit": limit, "q": q, "disponible": disponible}

from app.schemas.item import ItemCreate, ItemRead

FAKE_DB: dict[int, dict] = {}
_next_id = 1


@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    global _next_id
    item = {"id": _next_id, **payload.model_dump()}
    FAKE_DB[_next_id] = item
    _next_id += 1
    return item

from fastapi import HTTPException


@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int = Path(ge=1)):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return item

from fastapi import Response


@app.delete("/items/{item_id}", status_code=204, response_class=Response)
def delete_item(item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    del FAKE_DB[item_id]

"""""