# app/routers/items.py
from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

FAKE_DB: dict[int, dict] = {}

@router.get("/items/{item_id}")
def get_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}


@router.get("", response_model=list[ItemRead])
@router.get("/items")

@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int = Path(ge=1), payload: ItemUpdate = None):
    item = FAKE_DB.get(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} introuvable"
        )

    data = payload.model_dump(exclude_unset=True)
    item.update(data)

    return item

@router.put("/{item_id}", response_model=ItemRead)
def replace_item(item_id: int = Path(ge=1), payload: ItemCreate = None):
    item = FAKE_DB.get(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} introuvable"
        )

    item.update(payload.model_dump())

    return item

def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
    disponible: bool | None = None,
):
    return {"skip": skip, "limit": limit, "q": q, "disponible": disponible}



FAKE_DB: dict[int, dict] = {}
_next_id = 1


@router.post("/items", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    global _next_id
    item = {"id": _next_id, **payload.model_dump()}
    FAKE_DB[_next_id] = item
    _next_id += 1
    return item




@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int = Path(ge=1)):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return item

from fastapi import Response


@router.delete("/items/{item_id}", status_code=204, response_class=Response)
def delete_item(item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    del FAKE_DB[item_id]