from datetime import datetime

from domain.launch import Launch


class SpacexLaunchParser:

    @staticmethod
    def parse_all(data: list[dict]) -> list[Launch]:
        launches: list[Launch] = []

        try:
            for launch_data in data:
                utc_str: str = launch_data["date_utc"]
                utc = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))

                launch = Launch(
                    id = launch_data["id"],
                    mission_name = launch_data["name"],
                    details = launch_data["details"],
                    flight_number = launch_data["flight_number"],
                    launch_date = utc,
                    success = launch_data["success"],
                    upcoming = launch_data["upcoming"]
                )
                
                launches.append(launch)

        except Exception as e:
            print(f"Error parsing spacex launch data {e}")

        return launches
