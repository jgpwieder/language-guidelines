import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse
from gateways.database import DatabaseGateway

entityName = "flask_users"
app = FastAPI()


class User(BaseModel):

    id: str | None = None
    name: str
    nickname: str
    birth: str


@app.get("/users/{userId}")
async def read_user(userId: str):
    connection, errors = DatabaseGateway.createConnection()
    if errors:
        errorResponse = JSONResponse(content={
            "errors": [{
                "code": "internalServerError",
                "message": "Huston, we have a problem!",
            }]
        }, status_code=500)
        raise HTTPException(status_code=500, detail=errorResponse)

    result, getErrors = DatabaseGateway.getEntityById(connection=connection, entityName=entityName, entityId=userId)
    if getErrors:
        errorResponse = JSONResponse(content={"errors": getErrors}, status_code=400)
        raise HTTPException(status_code=400, detail=errorResponse)

    if result:
        return result

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/users/")
async def getUsers(limit: int = 10):
    connection, errors = DatabaseGateway.createConnection()
    if errors:
        errorResponse = JSONResponse(content={
            "errors": [{
                "code": "internalServerError",
                "message": "Huston, we have a problem!",
            }]
        }, status_code=500)
        raise HTTPException(status_code=500, detail=errorResponse)

    result, getErrors = DatabaseGateway.getAll(connection=connection, entityName=entityName)
    if getErrors:
        errorResponse = JSONResponse(content={"errors": getErrors}, status_code=400)
        raise HTTPException(status_code=400, detail=errorResponse)

    return result


@app.post("/users/")
async def createUser(user: User):
    connection, errors = DatabaseGateway.createConnection()
    if errors:
        errorResponse = JSONResponse(content={
            "errors": [{
                "code": "internalServerError",
                "message": "Huston, we have a problem!",
            }]
        }, status_code=500)
        raise HTTPException(status_code=500, detail=errorResponse)

    userJson = user.model_dump()
    result, postErrors = DatabaseGateway.createEntity(connection=connection, entityName=entityName, entity=userJson)
    if postErrors:
        errorResponse = JSONResponse(content={"errors": postErrors}, status_code=400)
        raise HTTPException(status_code=400, detail=errorResponse)

    return result


if __name__ == "__main__":
    connection, errors = DatabaseGateway.createConnection()
    entityName, modelErrors = DatabaseGateway.createModel(connection=connection, entityName=entityName)
    if modelErrors:
        raise Exception(modelErrors)

    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4,
        loop="auto",
        http="auto",
        interface="auto",
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()
