from http import HTTPStatus
from unittest.mock import patch
from unittest.mock import MagicMock

from domain.launch import Launch
from request.spacex import SpacexRequest
from parser.spacex import SpacexLaunchParser

@patch("request.spacex.requests.get")
def test_spacex_parser_launch(mock_get: MagicMock):
    
    mock_response = mock_get.return_value
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = [{
        "id": "123abc",
        "name": "name",
        "date_utc": "2006-03-24T22:30:00.000Z",
        "flight_number": 1,
        "success": True,
        "upcoming": True,
        "details": "details",
        "links": {
            "patch": {"small": "2"},
            "webcast": "1"
        }
        
    }]

    spacex_request = SpacexRequest()
    response = spacex_request.get_launches()

    launches = SpacexLaunchParser.parse_all(response)    
    launch = launches[0]

    assert len(launches) == 1
    assert isinstance(launches[0], Launch)
    assert launch.id == "123abc"
    assert launch.mission_name == "name"
    assert launch.launch_date.isoformat() == "2006-03-24T22:30:00+00:00"
    assert launch.success is True
    assert launch.upcoming is True
    assert launch.flight_number == 1
    assert launch.details == "details"
    assert launch.webcast_url == "1"
    assert launch.image_url == "2"
    