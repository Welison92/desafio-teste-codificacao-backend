# Imports de terceiros
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# Imports locais
from core.exceptions import APIException
from src.auth.routers import router as auth_router
from src.clients.routers import router as client_router
from src.orders.routers import router as order_router
from src.products.routers import router as product_router

# Inicialização do FastAPI
app = FastAPI(
    title="Lu Estilo API",
    version="1.0.0"
)

# Monta a pasta 'static' para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

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
app.include_router(client_router)
app.include_router(product_router)
app.include_router(order_router)


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
