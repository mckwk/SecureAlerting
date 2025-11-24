from typing import Optional


class ValidationUtils:

    @staticmethod
    def has_value_or_raise(value: Optional[object]) -> None:
        if not value:
            raise ValueError("Value cannot be None")