import dataclasses


@dataclasses.dataclass
class CreatedUser:
    id: int
    first_name: str
    last_name: str
    email: str
