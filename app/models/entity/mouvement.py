# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Mouvement(Entity):
    id: int = 0
    date: str = ""
    material_id: str = ""
    type: str = ""
    count: int = 0