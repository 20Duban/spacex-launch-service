from datetime import datetime
from unittest.mock import patch
from unittest.mock import MagicMock

from domain.launch import Launch
from services.launch import LaunchService

@patch("services.launch.SpacexRequest")
@patch("services.launch.SpacexLaunchParser")
def test_get_launch_service(
    mock_parser: MagicMock,
    mock_request: MagicMock
):
    
    fake_launches = [
        Launch(
            id="123abc",
            details="details",
            flight_number=1,
            launch_date=datetime.fromisoformat("2006-03-24T22:30:00+00:00"),
            mission_name="name",
            success=True,
            upcoming=True,
            webcast_url = "1",
            image_url = "2"
        )
    ]

    mock_request.get_launches.return_value = [{}]
    mock_parser.parse_all.return_value = fake_launches

    # repository
    fake_repository = MagicMock()
    fake_repository.upsert.return_value = True

    service = LaunchService(fake_repository)
    launches = service.get_launches()
    launch = launches[0]

    assert isinstance(launches, list)
    assert len(launches) == 1
    assert isinstance(launches[0], Launch)
    assert launch.id == "123abc"
    assert launch.details == "details"
    assert launch.flight_number == 1
    assert launch.launch_date.isoformat() == "2006-03-24T22:30:00+00:00"
    assert launch.mission_name == "name"
    assert launch.success == True
    assert launch.upcoming == True
    assert launch.webcast_url == "1"
    assert launch.image_url == "2"