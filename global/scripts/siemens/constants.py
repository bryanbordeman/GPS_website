# constants.py

# acceptable pressure drop (mbar)
ACCEPTABLE_PRESSURE_DROP = 100

TUBE_TYPE_LIST = {
    1: 'straight smooth',
    2: 'straight flexible',
    3: '45 deg smooth',
    4: '90 deg smooth',
    5: '45 deg segmented',
    6: '90 deg segmented',
    7: '90 deg mitred',
    }

TUBE_DIAMETERS = [
    '4',
    '6',
    '8',
    '10',
    '12',
    '14',
    '16',
]

LENGTH_MULTIPLIERS = [0.0 , 0.0, 1.0, 1.5, 1.7, 2.5, 8.3]

MAGNET_STRENGTH = [ '1.5T', '3.0T']

PI = 3.141592


MASS_FLOW_RATE = 2.07 #(kg.s-1)
INLET_TEMPERATURE = 12 #(K)
OUTLET_TEMPERATURE = 80 #(K)
OUTLET_PRESSURE = 101300 #(Pa)
OUTLET_DENSITY = 0.6085 #(kg.m-3)

