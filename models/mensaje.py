from dataclasses import dataclass
from typing import Optional, Any
import re


@dataclass
class Mensaje:
    id_chat: int  # Id del chat a donde será reenviado
    id_mensaje: int
    botones: Optional[Any]
    horario: str
    codigo: int  # Codigo identificador del mensaje programado



def generar_codigo(lista: list[Mensaje]) -> int:
    codigos_existentes = [msg.codigo for msg in lista]
    if not codigos_existentes:
        return 1
    return max(codigos_existentes) + 1

def validar_horario(horario: str) -> bool:
    match = re.fullmatch("^[LMXJVSD*]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", horario)
    if match is None:
        return False
    return True
