from typing import List

UNIQUE_ERR = "unique"

class ValidateError:
    value: str
    type: List[str]

    def __init__(self, value, type):
        self.value = value
        self.type = type
