from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import SecuritySchemeType
from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi

from app.api.routes import account

tags_metadata = [
    {
        "name": "Account",
        "description": "This is a list of interfaces containing account functionalities such as login and registering users.",
    }
]

# define the API application instance  - starting point to the app.
app = FastAPI(
    title="Sport Profles API",
    description="RESTful API web service for the Sports Profile (SP) social networking application.<br/><br/>Author: Marc Manuel<br/><br/>Note: this version uses Python 3.9, fastAPI, and SQLAlchemy with a SQL Server database.<br/>To experiment with the API functionalities, please send email to <b>marc_manuel@hotmail.com</b> to obtain test account and instructions.",
    version="1.0.0",
    docs_url="/docs",       # Default Swagger UI
    redoc_url="/redoc",     # ReDoc UI
    openapi_url="/openapi.json",  # JSON schema
    openapi_tags=tags_metadata
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bearer_scheme = HTTPBearer()

# Custom OpenAPI with security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=tags_metadata
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(account.router, prefix="/api")