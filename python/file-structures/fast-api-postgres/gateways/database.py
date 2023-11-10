import sys
import uuid
import logging
from psycopg2 import sql, pool, connect
from utils.erros import ApiError, ApiErrorCode, ApiErrorMessage
from utils.constants import databasePort, databaseUser, databaseHost, databasePassword, databaseName


class DatabaseGateway:

    _names = set()
    _connections = []
    _connectionPool = None

    @classmethod
    def createConnection(cls, name=None, password=None, user=None, port=None, host=None, autocommit=True):
        connection = connect(
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
    def createPool(cls, minConnections, maxConnections, name=None, password=None, user=None, port=None, host=None):
        cls._connectionPool = pool.SimpleConnectionPool(
            minConnections,
            maxConnections,
            database=name or databaseName,
            password=password or databasePassword,
            port=port or databasePort,
            host=host or databaseHost,
            user=user or databaseUser,
        )
        logging.info(f"CREATED connection pool: {cls._connectionPool}")

        return cls._connectionPool

    @classmethod
    def deallocatePoolConnection(cls, connection):
        cls._connectionPool.putconn(connection)
        logging.info(f"COSED connection from pool: {connection}")

    @classmethod
    def allocatePoolConnection(cls):
        print("ALLOC    ->    !!!!!")
        sys.stdout.flush()
        c = cls._connectionPool.getconn()
        logging.info(f"ALLOCATED connection from pool: {c}")
        return c

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

        cls._connectionPool.closeall()
        cls._connectionPool = None

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
        query = sql.SQL(f"""
            CREATE TABLE IF NOT EXISTS {entityName} (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(50),
                nickname VARCHAR(50),
                birth VARCHAR(50)
            )
        """)
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
