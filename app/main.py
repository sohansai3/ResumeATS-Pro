from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.db.session import Base, engine
from app.ui.routes import router as ui_router

configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="Resume ATS scoring service with PDF extraction, skill matching, dashboard, and downloadable reports.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix="/api/v1")
app.include_router(ui_router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("application_started", extra={"app_name": settings.app_name})


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "resume-ats-analyzer"}


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    logger.warning("validation_error", extra={"path": request.url.path, "errors": exc.errors()})
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("database_error", extra={"path": request.url.path})
    return JSONResponse(status_code=500, content={"detail": "A database error occurred."})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_error", extra={"path": request.url.path})
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})
