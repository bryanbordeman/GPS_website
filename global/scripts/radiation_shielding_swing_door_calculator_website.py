'''==========================================
Title:  radiation_shielding_swing_door_calculator_website.py
Author: Bryan Bordeman
Date:   051421
Revision: 0
;=========================================='''

import math

# ** const global variable **
STEEL_WEIGHT_CU_FT = 490 #standard carbon steel

def main():
    door_lead_shielding = float (input('enter lead thickness (in): '))
    door_bpe_shielding = float (input('enter 5% Borated Polyethylene thickness (in): '))

    door = Door(door_lead_shielding, door_bpe_shielding)
    # print(door.DOOR_LEAF_WIDTH_APPX )
    print(f'Hinge = {door.hinge_size.item_number}')

    if door.hinge_size.item_number != 'No hinge available. Exceeds maximum weight limit of this calculator':
        print(f'Operator = {door.operator.item_number}')
        print(f'Width = {door.total_door_leaf_width}')
        print(f'Width minus backset= {door.door_leaf_width}')
        print(f'Height = {door.DOOR_LEAF_HEIGHT}')
        print(f'Thickness = {door.door_leaf_thickness}')
        print(f'Strike Overlap = {door.door_overlap_strike}')
        print(f'Hinge Overlap = {door.DOOR_OVERLAP_HINGE}')
        print(f'Door Backset = {door.door_leaf_backset}')
        print(f'Appx weight = {door.appx_weight}')
        print(f'Shielding weight = {door.shielding_weight}')
        print(f'Lead Weight = {door.lead_total_weight}')
        print(f'Total Steel Weight = {door.total_door_shell_weight}')
        print(f'Door total weight = {door.door_leaf_actual_weight}')
        print(f'Radial Load = {door.max_radial_load}')
        print(f'ANSI Speed = {door.ansi_closing_time}')
        print(f'Check Radial Load = {door.radial_load_check}')


class Door:
    '''Door leaf object'''
    def __init__(self, door_lead_shielding, door_bpe_shielding):
        self.door_lead_shielding = door_lead_shielding
        self.door_bpe_shielding = door_bpe_shielding
        self.shielding_total_thickness = self.door_lead_shielding + self.door_bpe_shielding
        self.appx_door_width = self.shielding_total_thickness + 1.5 + 1 + 0.75 #1.5" for backer bar, 1" design gap, and 0.75" for face plates
    
        # ** const variable **
        self.LEAD_UNIT_WEIGHT = float (720) #unit = pounds/cubic/ foot
        self.BPE_UNIT_WEIGHT = (174/(4*8))*12 #unit = pounds/square/ foot
        self.DOOR_CLEAR_WIDTH = float (48) #unit = inches
        self.DOOR_CLEAR_HEIGHT = float (84) #unit = inches
        self.DESIGN_GAP_STRIKE = self.DESIGN_GAP_HINGE_SIDE = self.DESIGN_GAP_TOP = float(0.25) #unit - inches (gap between door leaf and frame)
        self.DESIGN_GAP_BOTTOM = float (0.75) #unit - inches (undercut on door leaf)
        self.DOOR_LEAF_HEIGHT = float((self.DOOR_CLEAR_HEIGHT + 4) - (self.DESIGN_GAP_TOP + self.DESIGN_GAP_BOTTOM)) #4" overlap on top of leaf
        self.DOOR_OVERLAP_HINGE = int(6) #6" overlap from door leaf on frame
        self.DOOR_OVERLAP_STRIKE_MIN = int(6) #6" overlap from door leaf on frame. this will change once final calc. are completed.

        #overlap will vary depending on the door thickness
        self.DOOR_LEAF_WIDTH = float(self.DOOR_CLEAR_WIDTH + (self.DOOR_OVERLAP_HINGE + self.DOOR_OVERLAP_STRIKE_MIN)) 
        
        temp_lead_shielding_weight = (((self.door_lead_shielding / 0.125) * 0.075) + 38.0625) * (self.door_lead_shielding * (self.LEAD_UNIT_WEIGHT/12)) 
        temp_bpe_shielding_weight = (((self.door_bpe_shielding / 0.125) * 0.075) + 38.0625) * (self.door_bpe_shielding * (self.BPE_UNIT_WEIGHT/12)) 
        self.appx_weight = temp_lead_shielding_weight + temp_bpe_shielding_weight + 1000 #used to get hinge size only, 1000 lbs added for steel
        
        # #** order of operations **
        self.find_hinge_size()

        if isinstance(self.hinge_size, Hinge): #check if hinge size exceeds limits
            self.barrel_offset = self.hinge_size.barrel_offset
            self.backer_bar_thickness = self.hinge_size.backer_bar_thickness
            self.backer_bar_width = self.hinge_size.backer_bar_width
            self.radial_capacity = self.hinge_size.radial_capacity
            self.barrel_offset = self.hinge_size.barrel_offset
            self.bolt_diameter = self.hinge_size.bolt_diameter
        else:
            self.barrel_offset = int(0)
            self.backer_bar_thickness = int(0)
            self.backer_bar_width = int(0)
            self.radial_capacity = int(0)
            self.barrel_offset = int(0)
            self.bolt_diameter = int(0)

        self.find_face_plate_thickness()
        self.total_filler_thickness = (self.door_lead_shielding + self.door_bpe_shielding + self.backer_bar_thickness + 1)
        self.rail_width_calc()
        self.door_leaf_thickness = float (self.front_face_plate.plate_thickness + self.back_face_plate.plate_thickness + self.rail_width.bar_width)
        self.front_face_plate_width()
        self.find_backset()
        self.door_leaf_width() # minus the backset
        self.door_overlap_strike = self.DOOR_OVERLAP_STRIKE_MIN  + self.door_leaf_backset
        self.door_leaf_steel_weight()
        self.lead_total_weight = round ((self.door_lead_shielding * (self.LEAD_UNIT_WEIGHT/12)) * (((self.door_leaf_width  - (self.rail_width.bar_thickness * 2))*(self.DOOR_LEAF_HEIGHT - ((self.rail_width.bar_thickness * 2) + 0.5)))/144),2)
        self.bpe_total_weight = round ((self.door_bpe_shielding * (self.BPE_UNIT_WEIGHT/12)) * (((self.door_leaf_width - (self.rail_width.bar_thickness *2))*(self.DOOR_LEAF_HEIGHT - ((self.rail_width.bar_thickness*2) + 0.5)))/144),2)
        self.shielding_weight = self.lead_total_weight + self.bpe_total_weight

        self.door_leaf_actual_weight()
        self.find_operator()
        self.barrel_center_x()
        self.barrel_center_y()
        self.barrel_center_z()
        self.radial_load()
        self.ansi_closing_time()
        self.radial_load_check()


    def find_hinge_size (self):
        '''finds the best hinge'''
        W500_HD = Hinge(int (1000), int(400), float(0.375), float (0.735), float(0.5), float(2.00), 'W500_HD')
        W875_HD = Hinge(int (3000), int(1200), float(0.5), float (0.926), float(0.5), float(3.00), 'W875_HD')
        W100_HD = Hinge(int (4000), int(1630), float(0.625), float (1.115), float(0.5), float(3.00), 'W100_HD')
        W125_HD = Hinge(int (8000), int(3300), float(0.75), float (1.5630), float(0.75), float(4.00),'W125_HD' )
        W150_HD = Hinge(int (13000), int(6280), float(0.875), float (2.033), float(1.00), float(4.00), 'W150_HD')
        W200_HD = Hinge(int (20000), int(8800), float(1.0), float (2.282), float(1.00), float(6.00), 'W200_HD')
        W250_HD = Hinge(int (25000), int(14000), float(1.0), float (2.75), float(1.25), float(6.00), 'W250_HD')
        no_hinge = Hinge(int (1000000), int(0), float(0), float (0), float(0), float(0), 'No hinge available. Exceeds maximum weight limit of this calculator')

        hinge_list = [W500_HD, W875_HD, W100_HD, W125_HD, W150_HD, W200_HD, W250_HD, no_hinge]


        for i in hinge_list:    
            if self.appx_weight <= i.thrust_capacity:
                self.hinge_size = i
                break
            


    def find_operator(self):
        '''finds the best operator'''
        NB500 = Operator(int (1000), int (4500), int(66), 'NB500')
        NB1000 = Operator(int (2250), int (12000), int(66), 'NB1000')
        NB2000 = Operator(int (3000), int (20000), int(75), 'NB2000')
        NB2000_HD2 = Operator(int (6000), int(25000), range (75, 84), 'NB2000_HD2')

        operator_list = [NB500, NB1000, NB2000, NB2000_HD2]

        for i in operator_list:    
            if self.door_leaf_actual_weight <= i.max_door_weight:
                self.operator = i
                break
            else:
                self.operator = 'No operator available. Exceeds maximum weight limit of this calculator'


    def rail_width_calc(self):
        '''calculate rail width''' 
        # 3/4" x 1" cold rolled bar (all sizes standard stock)
        cr_steel_bar_34112 = Rails(float(0.75), float(1.5))
        cr_steel_bar_34158 = Rails(float(0.75), float(1.625))
        cr_steel_bar_34134 = Rails(float(0.75), float(1.75))
        # 3/4" x 2" cold rolled bar (all sizes standard stock)
        cr_steel_bar_342 = Rails(float(0.75), float(2.00))
        cr_steel_bar_34214 = Rails(float(0.75), float(2.25))
        cr_steel_bar_34212 = Rails(float(0.75), float(2.50))
        cr_steel_bar_34234 = Rails(float(0.75), float(2.75))
        # 3/4" x 3" cold rolled bar (all sizes standard stock)
        cr_steel_bar_343 = Rails(float(0.75), float(3.00))
        cr_steel_bar_34314 = Rails(float(0.75), float(3.25))
        cr_steel_bar_34312 = Rails(float(0.75), float(3.50))
        cr_steel_bar_34334 = Rails(float(0.75), float(3.75))
        # 3/4" x 4" cold rolled bar (all sizes standard stock)
        cr_steel_bar_344 = Rails(float(0.75), float(4.00))
        cr_steel_bar_34414 = Rails(float(0.75), float(4.25))
        cr_steel_bar_34412 = Rails(float(0.75), float(4.50))
        cr_steel_bar_34434 = Rails(float(0.75), float(4.75))
        # 3/4" x 5" cold rolled bar (all sizes standard stock)
        cr_steel_bar_345 = Rails(float(0.75), float(5.00))
        cr_steel_bar_34512 = Rails(float(0.75), float(5.50))
        # 3/4" x 6" cold rolled bar (all sizes standard stock)
        cr_steel_bar_346 = Rails(float(0.75), float(6.00))
        cr_steel_bar_34612 = Rails(float(0.75), float(6.50))
        # 3/4" x 7" cold rolled bar (all sizes standard stock)
        cr_steel_bar_347 = Rails(float(0.75), float(7.00))
        # 3/4" x 8" cold rolled bar (all sizes standard stock)
        cr_steel_bar_348 = Rails(float(0.75), float(8.00))
        # 3/4" x 9" cold rolled bar (all sizes standard stock)
        cr_steel_bar_349 = Rails(float(0.75), float(9.00))
        # 3/4" x 10" cold rolled bar (all sizes standard stock)
        cr_steel_bar_3410 = Rails(float(0.75), float(10.00))
        # 3/4" x 11" cold rolled bar (all sizes standard stock)
        cr_steel_bar_3411 = Rails(float(0.75), float(11.00))
        # 3/4" x 12" cold rolled bar (all sizes standard stock)
        cr_steel_bar_3412 = Rails(float(0.75), float(12.00))
        # 3/4" x 14" cold rolled bar (all sizes standard stock)
        cr_steel_bar_3414 = Rails(float(0.75), float(14.00))
        # 3/4" x 16" cold rolled bar (all sizes standard stock)
        cr_steel_bar_3416 = Rails(float(0.75), float(16.00))
        # 3/4" x 18" cold rolled bar (all sizes standard stock)
        cr_steel_bar_3418 = Rails(float(0.75), float(18.00))
        # 3/4" x 20" cold rolled bar (all sizes standard stock)
        cr_steel_bar_3420 = Rails(float(0.75), float(20.00))

        ''' all variables below for doors > 13000 lbs'''

        # 1" x 4" cold rolled bar (all sizes standard stock)
        cr_steel_bar_14 = Rails(float(1.00), float(4.00))
        cr_steel_bar_1414 = Rails(float(1.00), float(4.25))
        cr_steel_bar_1412 = Rails(float(1.00), float(4.50))
        cr_steel_bar_1434 = Rails(float(1.00), float(4.75))
        # 1" x 5" cold rolled bar (all sizes standard stock)
        cr_steel_bar_15 = Rails(float(1.00), float(5.00))
        cr_steel_bar_1512 = Rails(float(1.00), float(5.50))
        # 1" x 6" cold rolled bar (all sizes standard stock)
        cr_steel_bar_16 = Rails(float(1.00), float(6.00))
        cr_steel_bar_1612 = Rails(float(1.00), float(6.50))
        # 1" x 7" cold rolled bar (all sizes standard stock)
        cr_steel_bar_17 = Rails(float(1.00), float(7.00))
        cr_steel_bar_1712 = Rails(float(1.00), float(7.50))
        # 1" x 8" cold rolled bar (all sizes standard stock)
        cr_steel_bar_18 = Rails(float(1.00), float(8.00))
        # 1" x 9" cold rolled bar (all sizes standard stock)
        cr_steel_bar_19 = Rails(float(1.00), float(9.00))
        # 1" x 10" cold rolled bar (all sizes standard stock)
        cr_steel_bar_110 = Rails(float(1.00), float(10.00))
        # 1" x 11" cold rolled bar (all sizes standard stock)
        cr_steel_bar_111 = Rails(float(1.00), float(11.00))
        # 1" x 12" cold rolled bar (all sizes standard stock)
        cr_steel_bar_112 = Rails(float(1.00), float(12.00))
        # 1" x 14" cold rolled bar (all sizes standard stock)
        cr_steel_bar_114 = Rails(float(1.00), float(14.00))
        # 1" x 16" cold rolled bar (all sizes standard stock)
        cr_steel_bar_116 = Rails(float(1.00), float(16.00))
        # 1" x 18" cold rolled bar (all sizes standard stock)
        cr_steel_bar_118 = Rails(float(1.00), float(18.00))
        # 1" x 20" cold rolled bar (all sizes standard stock)
        cr_steel_bar_120 = Rails(float(1.00), float(20.00))

        rail_list = [cr_steel_bar_34112, cr_steel_bar_34158,
                    cr_steel_bar_34134, cr_steel_bar_342, cr_steel_bar_34214,
                    cr_steel_bar_34212, cr_steel_bar_34234, cr_steel_bar_343,
                    cr_steel_bar_34314, cr_steel_bar_34312, cr_steel_bar_34334,
                    cr_steel_bar_344, cr_steel_bar_34414, cr_steel_bar_34412, 
                    cr_steel_bar_34434, cr_steel_bar_345, cr_steel_bar_34512,
                    cr_steel_bar_346, cr_steel_bar_34612, cr_steel_bar_347,
                    cr_steel_bar_348, cr_steel_bar_349, cr_steel_bar_3410,
                    cr_steel_bar_3411, cr_steel_bar_3412, cr_steel_bar_3414,
                    cr_steel_bar_3416, cr_steel_bar_3418, cr_steel_bar_3420,
                    cr_steel_bar_14, cr_steel_bar_1414, cr_steel_bar_1412,
                    cr_steel_bar_1434, cr_steel_bar_15, cr_steel_bar_1512,
                    cr_steel_bar_16, cr_steel_bar_1612, cr_steel_bar_17,
                    cr_steel_bar_1712, cr_steel_bar_18, cr_steel_bar_19,
                    cr_steel_bar_110, cr_steel_bar_111, cr_steel_bar_112,
                    cr_steel_bar_114, cr_steel_bar_116, cr_steel_bar_118,
                    cr_steel_bar_120]

        for i in rail_list:    
            if self.total_filler_thickness <= i.bar_width:
                self.rail_width = i
                break
            else:
                self.rail_width = int(0)

    def find_face_plate_thickness(self):
        '''calculate front plate'''
        plate_025 = Plates(float(0.25))
        plate_0375= Plates(float(0.375))

        if self.hinge_size.item_number == 'W150_HD' or self.hinge_size.item_number == 'W200_HD' or self.hinge_size.item_number == 'W250_HD':
            self.front_face_plate = plate_0375
        else:
            self.front_face_plate = plate_025

        if self.hinge_size.item_number == 'W200_HD' or self.hinge_size.item_number == 'W250_HD':
            self.back_face_plate = plate_0375
        else:
            self.back_face_plate = plate_025

    def front_face_plate_width(self):
        if (float((self.DESIGN_GAP_HINGE_SIDE) + self.barrel_offset + self.door_leaf_thickness) > self.DOOR_OVERLAP_HINGE): 
            self.total_door_leaf_width = float((self.DESIGN_GAP_HINGE_SIDE/2)+ self.barrel_offset + self.door_leaf_thickness + self.DOOR_CLEAR_WIDTH + self.DOOR_OVERLAP_STRIKE_MIN - self.DESIGN_GAP_STRIKE)
        else: 
            self.total_door_leaf_width = self.DOOR_LEAF_WIDTH - (self.DESIGN_GAP_STRIKE + self.DESIGN_GAP_HINGE_SIDE)
   
    def find_backset(self):
        find_backset = ((self.barrel_offset + self.door_leaf_thickness)**2) + (self.total_door_leaf_width**2)
        door_leaf_backset = math.sqrt(find_backset) - self.total_door_leaf_width
        self.door_leaf_backset = round(door_leaf_backset, 3)

    def door_leaf_width(self):
        door_leaf_width = self.total_door_leaf_width - self.door_leaf_backset
        self.door_leaf_width = round(door_leaf_width, 3)

    def door_leaf_steel_weight(self):
        front_face_plate_weight = round((self.front_face_plate.plate_sq_ft_weight) * ((self.total_door_leaf_width * self.DOOR_LEAF_HEIGHT/144)), 2)
        back_face_plate_weight = round((self.back_face_plate.plate_sq_ft_weight) * ((self.door_leaf_width * self.DOOR_LEAF_HEIGHT)/144), 2)
        backer_bar_weight = round(((490/12) * self.backer_bar_thickness) * ((self.backer_bar_width * 82)/144), 2)
        side_rail_weight = round(((490/12) * self.rail_width.bar_thickness) * ((self.rail_width.bar_width * self.DOOR_LEAF_HEIGHT)/144), 2) #calc only accounts for single rail
        top_style_weight = round(((490/12) * self.rail_width.bar_thickness) * ((self.rail_width.bar_width * self.total_door_leaf_width)/144), 2) #calc only accounts for single rail
        total_door_shell_weight = round (front_face_plate_weight + back_face_plate_weight +  backer_bar_weight + (side_rail_weight * 2) + (top_style_weight * 2), 2)
        self.total_door_shell_weight = total_door_shell_weight
    
    def door_leaf_actual_weight(self):
        self.door_leaf_actual_weight = round(self.total_door_shell_weight + self.shielding_weight,2)

    def barrel_center_x(self):
        self.barrel_center_x = round(((self.door_leaf_width /2) + (self.DESIGN_GAP_HINGE_SIDE/2))/12, 2)
 
    def barrel_center_y(self):
        '''while (radial_load_check() == 'RADIAL CAPACITY OUT OF RANGE'):
            barrel_center_y = barrel_center_y - .01'''
        if (self.hinge_size.item_number == 'W250_HD'): 
            self.barrel_center_y = round((self.DOOR_LEAF_HEIGHT - 20)/12, 2)
        else: 
            self.barrel_center_y = round((self.DOOR_LEAF_HEIGHT - 17)/12, 2)
        
    def barrel_center_z(self):
        self.barrel_center_z = round((self.door_leaf_thickness /2)+ self.hinge_size.barrel_offset,2)

    def radial_load(self):
        p1a = (self.door_leaf_actual_weight * self.barrel_center_x) / self.barrel_center_y 
        #In plane radial load caused by moment arm of the door width
        p1b = 0
        #Sum of any other in plane radial loads (such as those caused by a seismic event)
        p2a = (self.door_leaf_actual_weight *(self.barrel_center_z/12)) / self.barrel_center_y 
        #Out of plane radial load caused by moment arm of very thick doors
        p2b = 0
        #Sum of any other out of plane radial loads (such as those caused by wind, seismic or blast)
        self.max_radial_load = round(math.sqrt(((p1a+p1b)**2) +((p2a+p2b)**2)),2)
       
    #radial load check 
    def radial_load_check(self):
        if (self.hinge_size.radial_capacity >= self.max_radial_load): 
            self.radial_load_check =  True
        else: 
            self.radial_load_check = False
        

    def ansi_closing_time(self):
        self.ansi_closing_time = round((self.door_leaf_width )*(self.door_leaf_actual_weight)**0.5/188,1)
        
                  
        

class Hinge:
    '''Brookfield Industries Hinges'''
    def __init__(self, thrust_capacity, radial_capacity, 
    bolt_diameter, barrel_offset, backer_bar_thickness, 
    backer_bar_width, item_number):
        self.thrust_capacity = thrust_capacity #unit = pounds
        self.radial_capacity = radial_capacity #unit = pounds
        self.bolt_diameter = bolt_diameter #unit = inches
        self.barrel_offset = barrel_offset #distance from center of hinge barrel to face of door
        self.backer_bar_thickness = backer_bar_thickness #backer bar thickness
        self.backer_bar_width = backer_bar_width #backer bar width
        self.item_number = item_number
    
    def __repr__(self):
        return self.item_number


class Operator:
    '''Brookfield Industries Operators'''
    def __init__(self, operating_torque, max_door_weight, max_door_width, item_number ):
        self.operating_torque = operating_torque #unit = pounds/ inches
        self.max_door_weight = max_door_weight #unit = pounds
        self.max_door_width = max_door_width #unit = inches
        self.item_number = item_number

    def __repr__(self):
        return self.item_number

class Rails:
    '''door stiles and rails'''
    def __init__(self, bar_thickness, bar_width):
        self.bar_thickness = bar_thickness #unit = inches
        self.bar_width = bar_width #unit = inches
        self.rail_sq_ft_weight = self.pounds_sq_ft()
    
    def pounds_sq_ft(self):
        return (((STEEL_WEIGHT_CU_FT/12)*self.bar_thickness)/12)*self.bar_width

    def __repr__(self):
        return f'{self.bar_thickness}" x {self.bar_width}" Cold Rolled Steel Bar ({round(self.rail_sq_ft_weight,2)} lbs/ft)'

class Plates:
    '''door face plates'''
    def __init__(self, plate_thickness):
        self.plate_thickness = plate_thickness #unit = inches
        self.plate_sq_ft_weight = self.pounds_sq_ft()
    
    def pounds_sq_ft(self):
        return ((STEEL_WEIGHT_CU_FT/12)*self.plate_thickness)



if __name__ == "__main__":
    main()