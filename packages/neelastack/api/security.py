from fastapi import APIRouter
router=APIRouter(prefix='/security',tags=['security'])
@router.get('')\ndef security(): return {'status':'enabled'}\n