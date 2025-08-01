from repositories.repository import IRepository
from parser.spacex import SpacexLaunchParser
from request.spacex import SpacexRequest
from domain.launch import Launch


class LaunchService:

    def __init__(
        self,
        repository: IRepository
    ):
        self.__spacex_request = SpacexRequest()
        self.__repository = repository

    def get_launches(self):
        response = self.__spacex_request.get_launches()
        launches = SpacexLaunchParser.parse_all(response)

        return launches

    def save_launches(self, launches: list[Launch]):
        
        inserted = 0
        updated = 0

        for launch in launches:
            is_new = self.__repository.upsert(launch)
            
            if is_new:
                inserted += 1
            else:
                updated += 1

        return {"inserted": inserted, "updated": updated}
