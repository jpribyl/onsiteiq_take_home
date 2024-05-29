import dataclasses


@dataclasses.dataclass
class Permission:
    id: int
    content_type_id: int
    codename: str


@dataclasses.dataclass
class UserObjectPermission:
    user_id: int
    object_id: int
    permission_id: int
    content_type: str
