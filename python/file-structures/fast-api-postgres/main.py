import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
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
    connection = DatabaseGateway.allocatePoolConnection()
    result, getErrors = DatabaseGateway.getEntityById(connection=connection, entityName=entityName, entityId=userId)
    DatabaseGateway.deallocatePoolConnection(connection)

    if getErrors:
        errorResponse = JSONResponse(content={"errors": getErrors}, status_code=400)
        raise HTTPException(status_code=400, detail=errorResponse)

    if result:
        return result

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/users/")
async def getUsers(limit: int = 10):
    connection = DatabaseGateway.allocatePoolConnection()
    result, getErrors = DatabaseGateway.getAll(connection=connection, entityName=entityName)
    DatabaseGateway.deallocatePoolConnection(connection)

    if getErrors:
        errorResponse = JSONResponse(content={"errors": getErrors}, status_code=400)
        raise HTTPException(status_code=400, detail=errorResponse)

    return result


@app.post("/users/")
async def createUser(user: User):
    userJson = user.model_dump()

    connection = DatabaseGateway.allocatePoolConnection()

    result, postErrors = DatabaseGateway.createEntity(connection=connection, entityName=entityName, entity=userJson)
    DatabaseGateway.deallocatePoolConnection(connection)

    if postErrors:
        errorResponse = JSONResponse(content={"errors": postErrors}, status_code=400)
        raise HTTPException(status_code=400, detail=errorResponse)

    return result


if __name__ == "__main__":
    connection, errors = DatabaseGateway.createConnection()

    entityName, modelErrors = DatabaseGateway.createModel(connection=connection, entityName=entityName)
    if modelErrors:
        raise Exception(modelErrors)

    DatabaseGateway.createPool(1, 2)
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
