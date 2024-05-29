import dataclasses


@dataclasses.dataclass
class User:
    id: int
    first_name: str
    last_name: str
    email: str


@dataclasses.dataclass
class UserGroup:
    id: int
    name: str
