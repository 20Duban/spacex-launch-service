from dataclasses import dataclass
from datetime import datetime


@dataclass
class Launch:
    id: str
    mission_name: str
    launch_date: datetime
    flight_number: int
    success: bool
    upcoming: bool
    details: str
    image_url: str
    webcast_url: str