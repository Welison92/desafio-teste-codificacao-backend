# Imports de terceiros
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# Imports locais
from core.exceptions import APIException
from src.routers.auth import router as auth_router

# Inicialização do FastAPI
app = FastAPI(
    title="Lu Estilo API",
    version="1.0.0"
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas/Controles
app.include_router(auth_router)


# Manipulador de exceções para APIException
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "status": exc.status,
            "message": exc.message,
            "code": exc.code,
            "description": exc.description,
            "data": exc.data
        }
    )