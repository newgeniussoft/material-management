# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Material(Entity):
    id: int = 0
    date: str = ""
    name: str = ""
    type: str = ""
    brand: str = ""
    model: str = ""
    accessory: str = ""
    state: str = ""
    fonctionality: str = ""
    motif: str = ""
    observation: str = ""
    count: int = 0