from fastapi import APIRouter
router=APIRouter(prefix='/rag',tags=['rag'])
@router.post('/search')\ndef search(q:str): return {'query':q,'results':[]}\n