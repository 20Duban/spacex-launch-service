from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LaunchStatus(str, Enum):
    UPCOMING = "upcoming"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Launch:
    id: str
    mission_name: str
    launch_date: datetime
    # status: LaunchStatus
    flight_number: int
    success: bool
    upcoming: bool
    details: str
