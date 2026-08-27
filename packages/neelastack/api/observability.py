from fastapi import APIRouter
router=APIRouter(prefix='/observability',tags=['observability'])
@router.get('')\ndef observability(): return {'status':'ready'}\n