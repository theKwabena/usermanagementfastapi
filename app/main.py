from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.roles import router as permissions_router
from app.routes.groups import router as admin_router
from app.routes.login import router as login_router
app = FastAPI(title="uManager Backend", version="0.0.1", description="The backend for uManager app", debug=False)


app.include_router(user_router)
app.include_router(permissions_router)
app.include_router(admin_router)
app.include_router(login_router)


