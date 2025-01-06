from fastapi import APIRouter, HTTPException, Body
from app.services.validator import JSONValidator

router = APIRouter()


@router.post("/validate", tags=["JSON Validation"])
def validate_json(payload: dict = Body(...)):
    validator = JSONValidator()
    result = validator.validate(payload)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result)
    return result
