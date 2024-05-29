import dataclasses


@dataclasses.dataclass
class ContentType:
    id: int
    app_label: str
    model: str
