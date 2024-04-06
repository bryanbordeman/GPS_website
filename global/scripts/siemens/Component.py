
from constants import TUBE_TYPE_LIST

class Component:
    def __init__(self, element_type, index_number=0, diameter=0, length=0):
        self.element_type = element_type
        self.index_number = index_number
        self.length = length
        self.diameter = diameter
        self.pressure_drop = self.pressure_drop()
    
    def pressure_drop(self):
        pass

    def __str__(self):
        tube_type = TUBE_TYPE_LIST[self.element_type]
        return f'Type: {tube_type}, diameter: {self.diameter}, Length: {round(self.length, 0)} mm'
