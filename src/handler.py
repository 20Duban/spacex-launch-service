import json

from repositories.database_factory import Databases
from repositories.repository import IRepository
from services.launch import LaunchService


def lambda_handler(event, context):
    repository = Databases.create()
    launch_service = LaunchService(repository)

    launches = launch_service.get_launches()
    summary = launch_service.save_launches(launches)

    body = {
        "summary": summary
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': '*'
        },
        "body": json.dumps(body)
    }

    return response


