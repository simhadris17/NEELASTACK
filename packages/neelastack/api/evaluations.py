from fastapi import APIRouter
router=APIRouter(prefix='/evaluations',tags=['evaluations'])
@router.get('')\ndef evaluations(): return {'status':'ready'}\n