from fastapi import FastAPI
from app.routes.json_validation import router as json_validation_router

fast_api_app_instance = FastAPI(
    title="Universal Validation Service", description="A generic data validation service"
)

# Include routers
fast_api_app_instance.include_router(json_validation_router, prefix="/api/v1/json")