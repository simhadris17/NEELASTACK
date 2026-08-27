from fastapi import APIRouter

router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("")
def memory():
    return {"items": []}
