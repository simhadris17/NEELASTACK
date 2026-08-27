from fastapi import APIRouter
router=APIRouter(prefix='/memory',tags=['memory'])
@router.get('')\ndef memory(): return {'items':[]}\n