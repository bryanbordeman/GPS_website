'''==========================================
Title:  siemens_quench_vent_calculator.py
Author: Bryan Bordeman
Date:   010324
Revision: 0
;=========================================='''

from QuenchInputHandler import QuenchInputHandler, Component
from constants import ACCEPTABLE_PRESSURE_DROP
from constants import TUBE_TYPE_LIST
from constants import TUBE_DIAMETERS
from constants import MAGNET_STRENGTH


# vibration_decoupler = Component()

def main():
    # Example usage:
    handler = QuenchInputHandler()
    handler.get_input()
    # print(handler.get_quench_run()['components_list'])
    # Print type_index for each component on separate lines
    for component in handler.get_quench_run()['components_list']:
        print(component)
        
if __name__ == "__main__":
    main()