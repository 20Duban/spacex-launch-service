import os
import boto3

from repositories.repository import IRepository
from domain.launch import Launch
from config.dynamodb import (
    REGION_NAME, 
    ACCESS_KEY,
    SECRET_KEY,
    DB_TABLE_NAME
)

class DynamoDB (IRepository):

    def __init__(self):
        self.__table_name = os.getenv("DB_TABLE_NAME", DB_TABLE_NAME)
        region_name = os.getenv("REGION_NAME", REGION_NAME)
        access = os.getenv("ACCESS_KEY", ACCESS_KEY)
        secret = os.getenv("SECRET_KEY", SECRET_KEY)
        port = os.getenv("DB_PORT", None)
        host = os.getenv("DB_HOST", None)

        if host and port:
            endpoint_url = f"http://{host}:{port}"

        else:
            secret = None
            access = None
            endpoint_url = None

        self.__dynamodb = boto3.resource(
            "dynamodb",
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=access,
            aws_secret_access_key=secret
        )

        self.__client = self.__dynamodb.meta.client
        self.__create_table_if_not_exists()
        self.__table = self.__dynamodb.Table(self.__table_name)

    def __create_table_if_not_exists(self):
        existing_tables = self.__client.list_tables()["TableNames"]
        if self.__table_name in existing_tables:
            return

        try:
            self.__dynamodb.create_table(
                TableName=self.__table_name,
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"}
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            ).wait_until_exists()

        except Exception as e:
            print(f"Error creating the table: {e}")

    def __parse(self, launch: Launch):
        item = {
            "id": launch.id,
            "mission_name": launch.mission_name,
            "details": launch.details,
            "flight_number": launch.flight_number,
            "launch_date": launch.launch_date.isoformat(),
            "success": launch.success,
            "upcoming": launch.upcoming
        }
        
        return item
        
    def upsert(self, launch: Launch) -> bool:
        item = self.__parse(launch)
        response = self.__table.get_item(Key={"id": launch.id})
        is_new = "Item" not in response
        self.__table.put_item(Item=item)

        return is_new

    def batch_upsert(self, launches: list[Launch]):
        with self.__table.batch_writer() as batch:
            for launch in launches:
                batch.put_item(self.__parse(launch))
