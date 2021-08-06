from enum import Enum
from typing import Any
from typing import List
from typing import Tuple


class EventType(Enum):

    OPEN = "open"
    CLICK = "click"

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """
        Returns True if the specified value is valid in the enum
        Returns False otherwise
        """
        return any(value == item.value for item in cls)

    @classmethod
    def choices(cls) -> List[Tuple[Any, Any]]:
        return [(item.value, item.name) for item in cls]
