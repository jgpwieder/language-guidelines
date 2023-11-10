

class ApiError:

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def json(self):
        return {
            "code": self.code,
            "message": self.message,
        }


class ApiErrorCode:

    invalidName = "invalidName"
    invalidConnection = "invalidConnection"


class ApiErrorMessage:

    connectionNotFound = "There are no connections with the name {name}"
    databaseExists = "There is already a database with the name {name}"
    connectionExists = "There is a open connection to {name}, please close it before creating a new one"
