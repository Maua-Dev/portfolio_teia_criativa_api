"""Convenções de chaves Dynamo (tabela base).

Tabela base:
  pk = USER | PROJECT
  sk = USER#<uuid> | PROJECT#<uuid>
"""

from enum import Enum
from typing import Any
from uuid import UUID

# Nomes dos atributos da tabela base (alinhados ao CDK: pk/sk)
PK_ATTR = "pk"
SK_ATTR = "sk"

STORAGE_KEY_ATTRS = (
    PK_ATTR, SK_ATTR,
)


# conforme forem expandindo a quantidade de entidades, adicionem a esse enum
class EntityKind(str, Enum):
    USER = "USER"
    PROJECT = "PROJECT"


def partition_key(kind: EntityKind) -> str:
    """PK da tabela base — coleção (se repete para todos os items)."""
    return kind.value


def sort_key(id: UUID, kind: EntityKind) -> str:
    """SK da tabela base — identidade única dentro da coleção."""
    return f"{kind.value}#{id}"


def strip_keys(item: dict[str, Any]) -> dict[str, Any]:
    """Remove atributos de storage (pk/sk) antes do model_validate."""
    return {k: v for k, v in item.items() if k not in STORAGE_KEY_ATTRS}
