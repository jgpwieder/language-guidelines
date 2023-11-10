import uuid
import psycopg2
from psycopg2 import sql
from utils.erros import ApiError, ApiErrorCode, ApiErrorMessage
from utils.constants import databasePort, databaseUser, databaseHost, databasePassword, databaseName


class DatabaseGateway:

    _names = set()
    _connections = []
    _pools = []

    @classmethod
    def createConnection(cls, name=None, password=None, user=None, port=None, host=None, autocommit=True):
        connection = psycopg2.connect(
            database=name or databaseName,
            password=password or databasePassword,
            port=port or databasePort,
            host=host or databaseHost,
            user=user or databaseUser,
        )

        connection.autocommit = autocommit
        cls._connections.append(connection)
        cls._names.add(name)

        return connection, []

    @classmethod
    def createPool(cls, name, password, minConnections, maxConnections, user=None, port=None, host=None):
        pool = psycopg2.pool.SimpleConnectionPool(
            minConnections, maxConnections,
            host=host, user=user, password=password, port=port, database=name
        )
        cls._pools.append(pool)
        return pool, []

    @classmethod
    def closeConnection(cls, connection):
        try:
            cls._connections.remove(connection)
        except ValueError:
            return connection, [ApiError(
                code=ApiErrorCode.invalidName,
                message=ApiErrorMessage.connectionNotFound.format(connection=connection),
            ).json()]

        connection.close()
        return connection, []

    @classmethod
    def closeAllConnections(cls):
        for connection in cls._connections:
            connection.close()

        cls._connections = []

        for pool in cls._pools:
            pool.closeall()

        cls._pools = []

    @classmethod
    def createDatabase(cls, connection, name):
        cursor = connection.cursor()
        if name in cls._names:
            return name, [ApiError(
                code=ApiErrorCode.invalidName,
                message=ApiErrorMessage.databaseExists.format(name=name),
            ).json()]

        try:
            cursor.execute(f"CREATE DATABASE {name}")
        except:
            return name, [ApiError(
                code=ApiErrorCode.invalidName,
                message=ApiErrorMessage.databaseExists.format(name=name),
            ).json()]

        cursor.close()
        return name, []

    @classmethod
    def createModel(cls, connection, entityName):
        # Implement database schema management using migrations instead of creating tables here
        cursor = connection.cursor()
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(50),
                nickname VARCHAR(50),
                birth VARCHAR(50)
            )
        """).format(sql.Identifier(entityName))
        cursor.execute(query)
        cursor.close()
        return entityName, []

    @classmethod
    def createEntity(cls, connection, entityName, entity):
        del entity["id"]
        columString = ", ".join(entity.keys())
        valueString = ", ".join(["%s"] * len(entity))

        query = f"""INSERT INTO "{entityName}" (id, {columString}) VALUES (%s, {valueString})"""

        entityId = str(uuid.uuid4())
        values = (entityId,) + tuple(entity.values())

        entity.update({"id": entityId})

        cursor = connection.cursor()
        print(f"query: {query}")
        print(f"values: {values}")
        cursor.execute(query, values)
        connection.commit()
        cursor.close()

        return entity, []

    @classmethod
    def getAll(cls, connection, entityName):
        query = f"SELECT * FROM {entityName}"

        cursor = connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        columnNames = [desc[0] for desc in cursor.description]
        return [dict(zip(columnNames, row)) for row in result], []

    @classmethod
    def getEntityById(cls, connection, entityName, entityId):
        query = f"SELECT * FROM {entityName} WHERE id = %s"

        cursor = connection.cursor()
        cursor.execute(query, (entityId,))

        result = cursor.fetchall()
        cursor.close()

        return dict(result), []

    @classmethod
    def getEntitiesByIds(cls, connection, entityName, entityIds):
        placeholders = ', '.join(['%s' for _ in entityIds])

        query = f"SELECT * FROM {entityName} WHERE id IN ({placeholders})"

        cursor = connection.cursor()
        cursor.execute(query, entityIds)

        result = cursor.fetchall()
        cursor.close()

        return result, []
