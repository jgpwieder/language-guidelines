from fastapi import HTTPException
from starlette.responses import JSONResponse


class HttpException:

    internalServerError = HTTPException(
        status_code=500,
        detail=JSONResponse(
            status_code=500,
            content={
                "errors": [{
                    "code": "internalServerError",
                    "message": "Huston, we have a problem!",
                }]
            },
        ))
