from constants import MAGNET_STRENGTH, TUBE_TYPE_LIST, TUBE_DIAMETERS, LENGTH_MULTIPLIERS
from Component import Component

#   lenght * LENGTH_MULTIPLIERS[index]+ dia_in_mm/127 * LENGTH_MULTIPLIERS[index]+ lenght

def inches_to_mm(inches):
    mm_per_inch = 25.4
    mm = inches * mm_per_inch
    return mm

class QuenchInputHandler:
    def __init__(self):
        self.quench_run = None

    def add_vibration_decoupler(self, diameter):
        # this is a vibration decoupler
        component = Component(element_type=2, diameter=diameter, length=inches_to_mm(14.625))
        return component

    def get_input(self):
        components_list = []

        while True:
            try:
                magnet = int(input('\n'.join([f'({i + 1} = {value})' for i, value in enumerate(MAGNET_STRENGTH)]) +
                    '\nSelect Magnet Strength: '))
                diameter = 0
                if(magnet == 1):
                    diameter = TUBE_DIAMETERS[0]
                elif (magnet == 2):
                    diameter = TUBE_DIAMETERS[1]

                components_list.append(self.add_vibration_decoupler(diameter))
                if magnet not in range(1, len(MAGNET_STRENGTH) + 1):
                    print('Invalid entry, out of range')
                    continue
                else:
                    break
            except ValueError:
                print('Invalid entry, enter integer')
                continue

        while True:
            try:
                temp_tube_type_list = {i: TUBE_TYPE_LIST[i] for i in TUBE_TYPE_LIST if i != 2}
                component_index = int(input('\n'.join([f'({i} = {temp_tube_type_list[i]})' for i in temp_tube_type_list]) +
                                    f'\n({max(temp_tube_type_list.keys()) + 1} = Calculate)'
                                    '\nSelect component: '))
                
                if component_index not in range(1, len(TUBE_TYPE_LIST) + 2):
                    print('Invalid entry, out of range')
                    continue

                length = 0
                if component_index == 1:    
                    length = inches_to_mm(int(input('Enter length (in): ')))

            except ValueError:
                print('Invalid entry, enter integer')
                continue

            if component_index == len(TUBE_TYPE_LIST) + 1:
                break
            else:
                component = Component(element_type=component_index, length=length)
                components_list.append(component)

        self.quench_run = {'components_list': components_list, 'magnet': magnet}

    def get_quench_run(self):
        return self.quench_run
    