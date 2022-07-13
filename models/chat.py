from dataclasses import dataclass


@dataclass
class Chat:
    id_chat: int
    nombre: str
    autorizado: bool
