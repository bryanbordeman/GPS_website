'''==========================================
Title:  ge_quench_vent_calculator.py
Author: Bryan Bordeman
Date:   032419
Revision: 0
;=========================================='''


def main():
    comp_function()

    display_list =['0-20 feet = ', '20-40 feet = ', '40-60 feet = ', '60-80 feet = ', '80-100 feet = ']
    for i in range(len(quench_run.pipe_size_location_list)):
        if quench_run.pipe_size_location_list[i] != 0:
            print(str(display_list[i]) + str(quench_run.pipe_size_location_list[i]))
    print('Total Pressure Drop = {}'.format(str(quench_run.total_pressure)))

def comp_function():
    '''only applicable if __name__ = __main__'''
    global quench_run
    comp_list = []
    strght_list = []
    while True:
        try:
            magnet = int(input('Magnet Strength: (1 = 1.5T) (2 = 3.0T): '))
            if magnet not in range(1, 3):
                continue
            else:
                break
        except ValueError:
            print('invalid entry, enter integer')
            continue
    while True:
        try:
            comp = int(input('Select component: (1 = Straight) (2 = 45 deg. Elbow) (3 = 90 deg. Elbow) (4 = Calculate): '))
            if comp not in range(1, 5):
                continue
        except ValueError:
            print('invalid entry, enter integer')
            continue
        if comp == 4:
            break
        else:
            comp_list.append(comp)
            if comp == 1:
                lgt = int(input('Enter length (in): '))
                strght_list.append(lgt)
    quench_run = GEQuench(comp_list, strght_list, magnet)
    return quench_run


class GEQuench:
    def __init__(self, comp_list, strght_list, magnet = 1):
        self.comp_list = comp_list
        self.strght_list = strght_list
        self.lgt_list = self.lgt_sort()
        self.magnet = magnet
        self.pressure_drop()

    def lgt_sort(self):
        '''Creates list of lengths every 20 feet'''
        lgt = 0
        lgt_list = []
        for i in self.strght_list:  # adds up list to total length
            lgt += i
        lgt = round(lgt / 12, 2)

        # any length below 20 feet
        if lgt <= 20:
            lgt_list.append(lgt)
            return lgt_list

        # any length above 20 feet
        elif lgt > 20:
            for i in range(20): #! changed from 5 to 20 for testing
                if lgt >= 20:
                    lgt_list.append(20)
                    remainder = lgt % (int(lgt / 20) * 20)
                    lgt -= 20
                else:
                    lgt_list.append(remainder)
                    return lgt_list

    def pressure_drop(self):
        '''Returns pressure drop and pipe sizes'''




        #---------------------GE 1.5T Pressure Drop Matrix----------------------
        # row [0] = 8" pipe, row [1] = 10" pipe, row [2] = 12" pipe, row [3] = 14" pipe, row [4] = 16" pipe
        # col [0] = Straight, col [1] = 45 deg elbow, col [2] = 90 deg elbow

        MATRIX_1_5T = [[[0.1, 0.55, 1.03],
                [0.03, 0.27, 0.41],
                [0.013, 0.14, 0.21],
                [0.008, 0.102, 0.15],
                [0.0053, 0.078, 0.115]],
               [[0.21, 1.03, 1.85],
                [0.07, 0.41, 0.75],
                [0.027, 0.21, 0.41],
                [0.017, 0.154, 0.30],
                [0.013, 0.188, 0.229]],
               [[0.30, 1.44, 2.60],
                [0.10, 0.62, 1.1],
                [0.041, 0.27, 0.55],
                [0.026, 0.198, 0.40],
                [0.02, 0.152, 0.306]],
               [[0.38, 1.85, 3.36],
                [0.12, 0.75, 1.37],
                [0.054, 0.34, 0.69],
                [0.034, 0.25, 0.51],
                [0.026, 0.191, 0.39]],
               [[0.47, 2.26, 4.11],
                [0.16, 0.96, 1.71],
                [0.069, 0.48, 0.75],
                [0.043, 0.353, 0.55],
                [0.033, 0.27, 0.421]]]

        #---------------------GE 3T Pressure Drop Matrix----------------------
        # row [0] = 8" pipe, row [1] = 10" pipe, row [2] = 12" pipe, row [3] = 14" pipe, row [4] = 16" pipe
        # col [0] = Straight, col [1] = 45 deg elbow, col [2] = 90 deg elbow
        # code needS to be modified for 8" pipe. per spec needs to be every 10' upto 60' max. code below averages pressure in 20' increments to fit algorithm used on 1.5T which is every 20'

        MATRIX_3T = [[[((0.14+0.24)/2), ((0.74+1.22)/2), ((1.4+2.29)/2)],
                [0.06, 0.41, 0.78],
                [0.02, 0.17, 0.32],
                [0.008, 0.087, 0.154],
                [0.004, 0.043, 0.081]],
                [[((0.36+0.47)/2), ((1.66+2.07)/2), ((3.11+3.88)/2)],
                [0.12, 0.70, 1.31],
                [0.041, 0.29, 0.54],
                [0.017, 0.137, 0.257],
                [0.008, 0.072, 0.135]],
                [[((0.57+0.65)/2), ((2.45+2.79)/2), ((4.58+5.24)/2)],
                [0.17, 0.95, 1.78],
                [0.06, 0.39, 0.74],
                [0.024, 0.187, 0.350],
                [0.011, 0.098, 0.184]],
                [[0, 0, 0],
                [0.21, 1.17, 2.19],
                [0.75, 0.49, 0.91],
                [0.031, 0.232, 0.435],
                [0.014, 0.122, 0.288]],
                [[0, 0, 0],
                [0.25, 1.36, 2.56],
                [0.88, 0.57, 1.07],
                [0.036, 0.272, 0.511],
                [0.017, 0.144, 0.269]]]


        # commented code below is for future integration of 3T 10' calculation.

        # MATRIX_3T = [[[0.14, 0.74, 1.4],
        #         [0.24, 1.22, 2.29]
        #         [0.06, 0.41, 0.78],
        #         [0.06, 0.41, 0.78],
        #         [0.02, 0.17, 0.32],
        #         [0.02, 0.17, 0.32],
        #         [0.008, 0.087, 0.154],
        #         [0.008, 0.087, 0.154],
        #         [0.004, 0.043, 0.081],
        #         [0.004, 0.043, 0.081]],
        #         [[0.36, 1.66, 3.11],
        #         [0.47, 2.07, 3.88]
        #         [0.12, 0.70, 1.31],
        #         [0.12, 0.70, 1.31],
        #         [0.041, 0.29, 0.54],
        #         [0.041, 0.29, 0.54],
        #         [0.017, 0.137, 0.257],
        #         [0.017, 0.137, 0.257],
        #         [0.008, 0.072, 0.135],
        #         [0.008, 0.072, 0.135]],
        #         [[0.57, 2.45, 4.58],
        #         [0.65, 2.79, 5.24]
        #         [0.17, 0.95, 1.78],
        #         [0.17, 0.95, 1.78],
        #         [0.06, 0.39, 0.74],
        #         [0.06, 0.39, 0.74],
        #         [0.024, 0.187, 0.350],
        #         [0.024, 0.187, 0.350],
        #         [0.011, 0.098, 0.184],
        #         [0.011, 0.098, 0.184]],
        #         [[0, 0, 0],
        #         [0, 0, 0],
        #         [0.21, 1.17, 2.19],
        #         [0.21, 1.17, 2.19],
        #         [0.75, 0.49, 0.91],
        #         [0.75, 0.49, 0.91],
        #         [0.031, 0.232, 0.435],
        #         [0.031, 0.232, 0.435],
        #         [0.014, 0.122, 0.288],
        #         [0.014, 0.122, 0.288]],
        #         [[0, 0, 0],
        #         [0, 0, 0],
        #         [0.25, 1.36, 2.56],
        #         [0.25, 1.36, 2.56],
        #         [0.88, 0.57, 1.07],
        #         [0.88, 0.57, 1.07],
        #         [0.036, 0.272, 0.511],
        #         [0.036, 0.272, 0.511],
        #         [0.017, 0.144, 0.269],
        #         [0.017, 0.144, 0.269]]]

        if self.magnet == 1:
            matrix = MATRIX_1_5T
            pressure_limit = 17
        else:
            matrix = MATRIX_3T
            pressure_limit = 20

        #-------------------------------------------------------------------------
        # sets all straight pressures

        # size_list works as stated below
        # first dimension  = [0] = 8" dia, [1] = 10" dia, [2] = 12" dia, [3] = 14" dia, [4] = 16" dia
        # second dimension = [0] = 0-20ft, [1] = 20-40ft, [2] = 40-60ft, [3] = 60-80ft, [4] = 80-100ft
        size_list = [[0] * len(self.lgt_list) for i in range(5)]

        
        for i in range(len(self.lgt_list)):
            for j in range(len(size_list)):
                size_list[j][i] = (round(self.lgt_list[i] * (matrix[i][j][0]), 2))

        # sets all components

        strght = 0

        # makes empty list
        comp_matrix = [[[0 for k in range(0)] for j in range(5)] for i in range(5)]
        # print(comp_matrix)

        for i in self.comp_list:
            if i == 1:
                strght += self.strght_list.pop(0) / 12

            if strght <= 20:
                k = 0
            if strght > 20 and strght <= 40:
                k = 1
            if strght > 40 and strght <= 60:
                k = 2
            if strght > 60 and strght <= 80:
                k = 3
            if strght > 80 and strght <= 100:
                k = 4

            for j in range(5):
                if i == 2:
                    comp_matrix[j][k].append(matrix[k][j][1])
                if i == 3:
                    comp_matrix[j][k].append(matrix[k][j][2])
            # print(comp_matrix)

        # adds pressure from straights to components in appropriate section of length
        # makes empty list
        pressure_matrix = [[[0 for k in range(0)] for j in range(5)] for i in range(5)]
        # print(pressure_matrix)

        for i in range(5):
            for j in range(5):
                temp = 0
                if len(size_list[j]) > i:
                    for m in comp_matrix[j][i]:  # 3d matrix
                        temp += m
                    temp += size_list[j][i]  # 2d matrix
                    pressure_matrix[i][j] = temp
        # print(pressure_matrix)

        pipe_size_list = ['8" dia pipe', '10" dia pipe', '12" dia pipe', '14" dia pipe', '16" dia pipe']
        self.total_pressure = 0
        self.pipe_size_location_list = [0 for i in range(5)]

        # creates blank list
        idx_list = [0 for i in range(5)]
        


        # makes list of added pressure from 8" dia (index[0]) upto to 16" dia(index[4])
        for i in range(3): #! run 3 times to adjust for pressure being over limit on first few trys

            pressure_list_matrix = [[0 for j in range(5)] for i in range(5)]
            for i in range(5):
                for j in range(5):
                    pressure_list_matrix[i][j] = pressure_matrix[i][j]

            # returns pipe size string as well as updates the pressure drop

            # below loop should be combined into one loop
            if len(self.lgt_list) > 0:

                for i in range(len(pressure_list_matrix[0])):
                    if pressure_list_matrix[0][idx_list[0]] <= pressure_limit:
                        self.total_pressure = pressure_list_matrix[0][idx_list[0]]
                        self.pipe_size_location_list[0] = pipe_size_list[idx_list[0]]
                        # print(idx_list)
                      
                        break
                    else:
                        idx_list[0] += 1
                        # print(idx_list)
                        continue
            
            
            for i in range(1,5):
                if len(self.lgt_list) > i:

                    #! this needs to loop back if bust!!!
                    if idx_list[i-1] > 0:
                        idx_list[i] = idx_list[i-1]

                    for j in range(len(pressure_list_matrix[i])):
                        if (pressure_list_matrix[i][idx_list[i]] + self.total_pressure) <= pressure_limit:
                            self.total_pressure += pressure_list_matrix[i][idx_list[i]]
                            self.pipe_size_location_list[i] = pipe_size_list[idx_list[i]]
                            break
                        else:
                            idx_list[i] += 1
                            print(idx_list)
                            continue

        return self.pipe_size_location_list, self.total_pressure

if __name__ == "__main__":
    main()


# Test Below passed (03/19/19)

# Inputs
# Straight 120" long
# 45 deg. Elbow
# 90 deg. Elbow
# Straight 500" long
# 90 deg. Elbow
# 90 deg. Elbow
# Straight 120" long

# Results at 1.5T (Pressure = 12.18)
# 0-20 feet = 8" Pipe
# 20-40 feet = 8" Pipe
# 40-60 feet = 10" Pipe
# 60-80 feet = 10" Pipe

# notes need to make error message if pipe input exceeds 100 feet.

# Inputs (bust!!)
# Straight 120" long
# 45 deg. Elbow
# 90 deg. Elbow
# Straight 500" long
# 90 deg. Elbow
# 90 deg. Elbow
# Straight 345" long
# 90 deg. Elbow
# Straight 345" long