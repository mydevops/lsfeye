from enum import Enum
from enum import unique


@unique
class ApiVersion(Enum):
    VERSION_1 = 1
    VERSION_2 = 2
    VERSION_3 = 3
    VERSION_4 = 4
    VERSION_5 = 5


@unique
class HTTPStatusCode(Enum):
    SUCCESS = 0
    FAILURE = -1


@unique
class AlarmNotificationType(str, Enum):
    DINGDING = "dingding"
