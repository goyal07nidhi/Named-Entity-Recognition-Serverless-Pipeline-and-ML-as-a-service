from fastapi import APIRouter
from .endpoints import access, ner, MaskedAndAnonymized

router = APIRouter()
router.include_router(access.router, tags =["access"])
router.include_router(ner.router, tags =["ner"])
router.include_router(MaskedAndAnonymized.router, tags =["mask_anonymize"])