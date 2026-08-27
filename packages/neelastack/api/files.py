from fastapi import APIRouter
router=APIRouter(prefix='/files',tags=['files'])
@router.get('')\ndef files(): return []\n