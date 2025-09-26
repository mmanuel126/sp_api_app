# app/main.py
# This module serves as the main entry point for the Sport Profiles API application, which is a RESTful backend for a social networking platform. It:
# Initializes the FastAPI application.
# Adds middleware for CORS and static file handling.
# Registers multiple API routers for feature domains like:
# * Account
# * Common
# * Contact
# * Member
# * Message
# * Setting
# * Configures OAuth2 / Bearer JWT security for protected routes.
# * Customizes Swagger/OpenAPI documentation with grouped tags and security definitions.

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import SecuritySchemeType
from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi

from app.api.routes import account, common, contact, member, message, setting
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# organizes API endpoints into meaningful sections in SWagger docs
tags_metadata = [
    {
        "name": "Account",
        "description": "This is a list of interfaces containing account functionalities such as login and registering users.",
    },
    {
        "name": "Common",
        "description": "This is a collection of common interfaces and shared functionalities used by the SP.",
    },
    {
        "name": "Contact",
        "description": "Contains API functionalities to manage and control member contacts.",
    },
    {
        "name": "Member",
        "description": "Contains member management API functionalities.",
    },
    {
        "name": "Message",
        "description": "Contains API functionalities for messaging or communication between members.",
    },
    {
        "name": "Setting",
        "description": "This is a list of interfaces to manage application settings and user preferences.",
    },
]

# define the API application instance  - starting point to the app.
app = FastAPI(
    title="Sport Profles API",
    description="""RESTful API web service for the Sports Profile (SP) social networking application.<br/><br/>
Author: <b>Marc Manuel</b> (https://www.linkedin.com/in/marc-manuel-b298326/)<br/><br/>
Note: This version uses Python 3.9, fastAPI, and SQLAlchemy with a SQL Server database.<br/>
<div>
  <h3>Quick Start with Swagger</h3>
  <ol>
    <li>Go to <code>/api/account/Login</code> under the <strong>Account</strong> service.</li>
    <li>Login with:
      <ul>
        <li><strong>Email:</strong> <code>michael.jordan@outlook.com</code></li>
        <li><strong>Password:</strong> <code>123456</code></li>
      </ul>
    </li>
    <li>Copy the JWT token from the response.</li>
    <li>Click <strong>"Authorize"</strong> and enter:
      <pre><code>&lt;your_JWT_token&gt;</code></pre>
    </li>
    <li>You're now ready to access secured endpoints.</li>
  </ol>
</div>
<p>You can also create an account using the <a href="https://react-sport-profiles.vercel.app/login" target="_blank">React web application</a> that consumes this API service.</p>
""",
    version="1.0.0",
    docs_url="/docs",  # Default Swagger UI
    redoc_url="/redoc",  # ReDoc UI
    openapi_url="/openapi.json",  # JSON schema
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "docExpansion": "none",  # Collapse all endpoints
        "defaultModelsExpandDepth": 1,  # do not Hide models section but don't expand
    },
)

# use the commented code below to catch and log validatoin errors

# @app.exception_handler(RequestValidationError)
# async def custom_validation_handler(request: Request, exc: RequestValidationError):
#    print("Validation error details:", exc.errors())
#    return await request_validation_exception_handler(request, exc)

#serves files (images, JS, CSS, etc) from /static URL path
app.mount("/static", StaticFiles(directory="static"), name="static")

# allows cross-origin requests (e.g., from React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set specific domains ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#define autentication methods using OAuth2 with JWT bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bearer_scheme = HTTPBearer()


# Custom OpenAPI with security scheme - extends the generated OpenAPI schema to add a JWT Bearer security scheme and attach to every endpoit in hte schema.
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=tags_metadata,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

#registers all route modules under /api
app.include_router(account.router, prefix="/api")
app.include_router(common.router, prefix="/api")
app.include_router(contact.router, prefix="/api")
app.include_router(member.router, prefix="/api")
app.include_router(message.router, prefix="/api")
app.include_router(setting.router, prefix="/api")
