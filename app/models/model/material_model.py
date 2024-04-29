from ..entity import Material
from .base_model import Model

class MaterialModel(Model):
    def __init__(self):
        super().__init__("materials", Material())