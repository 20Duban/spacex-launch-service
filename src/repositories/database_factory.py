from typing import Optional
from abc import ABC, abstractmethod

from repositories.repository import IRepository
from repositories.dynamodb.dynamodb import DynamoDB


class DatabaseFactory:

    @abstractmethod
    def create_database(self) -> IRepository:
        pass


class DynamoDbFactory (DatabaseFactory):

    def create_database(self) -> IRepository:
        repository = DynamoDB()

        return repository


class Databases:

    @staticmethod
    def create(database_type: str = "dynamo") -> Optional[IRepository]:
        
        repository: IRepository = None

        if database_type == "dynamo":
            repository = DynamoDbFactory().create_database()
        
        return repository
