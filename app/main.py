from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user import router as user_router
from app.routes.roles import router as permissions_router
from app.routes.groups import router as admin_router
from app.routes.login import router as login_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="uManager Backend", version="0.0.1", description="The backend for uManager app", debug=False)

app.mount("/static", StaticFiles(directory='static'), name='static')


origins = ["http://localhost:3000", "http://localhost:8000", 'http://192.254.0.115:3000' ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(user_router)
app.include_router(permissions_router)
app.include_router(admin_router)
app.include_router(login_router)
