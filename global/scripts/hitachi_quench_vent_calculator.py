'''
==========================================
Title:  hitachi_oasis_quench_vent_calculator.py
Author: Bryan Bordeman
Date:   060819
Revision: 2
==========================================
'''
#-------------------Global Varibles-----------------------
compList = []
strghtList = []


#-------------------Main Function---------------------------


def main():
    comp_function()

    display_list = ['4" dia pipe', '6" dia pipe', '8" dia pipe']
    parts_list = ['Straight', '45 deg. Elbow', '90 deg. Elbow']
    for i in range(len(quench_run.comp_list)):
        print(parts_list[quench_run.comp_list[i] - 1] + ' = ' + display_list[quench_run.pipe_size_list[i]])
    print('Total Percentage = ' + str(round(quench_run.total_perc * 100, 2)) + '%')
    print('Total Length = ' + str(round(quench_run.total_lgt, 2)) + ' Feet')

    # print('Total Pressure Drop = {}'.format(str(quench_run.total_pressure)))

    # print(quench_run.temp, '\n')
    # print(quench_run.perc, '\n')
# print(quench_run.total_lgt, '\n')
# print(quench_run.pipe_size_list, '\n')
#

#-------------------Get Components--------------------------
def comp_function():
    '''only applicable if __name__ = __main__'''
    global quench_run
    comp_list = []
    strght_list = []
    # while True:
    #     try:
    #         magnet = int(input('Magnet Strength: (1 = 1.5T) (2 = 3.0T): '))
    #         if magnet not in range(1, 3):
    #             continue
    #         else:
    #             break
    #     except ValueError:
    #         print('invalid entry, enter integer')
    #         continue
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
    quench_run = HitachiQuench(comp_list, strght_list)
    # quench_run = Quench(comp_list, strght_list, magnet)
    return quench_run


class HitachiQuench:
    def __init__(self, comp_list, strght_list, field):
        # def __init__(self, comp_list, strght_list, magnet=1):
        self.comp_list = comp_list
        self.strght_list = strght_list
        self.field = field

        print(type(self.field))
        # self.lgt_list = self.lgt_sort()
        # self.magnet = magnet
        # self.pressure_drop()

        self.comp_sort()

        self.calculate(0, 0)

    def comp_sort(self):

        temp_index = 0
        self.total_lgt = 0
        self.total_perc = 0
        self.pipe_size_list = []

        if self.field == 2:
            #-------------------Hitachi Oasis 1.2T Varibles-----------------
            # index 0 = 4" dia pipe, index 1 = 6" dia pipe, index 2 = 8" dia pipe
            self.MAX_STRGHT = [18, 77, 226]
            self.ELBOW_45 = [round(30 / 12, 2), round(45 / 12, 2), round(62 / 12, 2)]
            self.ELBOW_90 = [round(45 / 12, 2), round(68 / 12, 2), round(96 / 12, 2)]
        else:
            #-------------------Hitachi Echelon 1.5T Varibles-----------------
            # index 0 = 4" dia pipe, index 1 = 6" dia pipe, index 2 = 8" dia pipe
            self.MAX_STRGHT = [30, 58, 171]
            self.ELBOW_45 = [round(43 / 12, 2), round(47 / 12, 2), round(71 / 12, 2)]
            self.ELBOW_90 = [round(67 / 12, 2), round(71 / 12, 2), round(106 / 12, 2)]

        #-------------------create list of lengths-----------------
        self.temp = [[0 for j in range(len(self.MAX_STRGHT))] for i in range(len(self.comp_list))]
        self.perc = [[0 for j in range(len(self.MAX_STRGHT))] for i in range(len(self.comp_list))]
        # self.temp = []

        for i in range(len(self.comp_list)):
            if self.comp_list[i] == 1:
                for j in range(len(self.MAX_STRGHT)):
                    self.temp[i][j] = self.strght_list[temp_index] / 12
                temp_index += 1

            elif self.comp_list[i] == 2:
                for j in range(len(self.ELBOW_45)):
                    self.temp[i][j] = self.ELBOW_45[j]

            elif self.comp_list[i] == 3:
                for j in range(len(self.ELBOW_90)):
                    self.temp[i][j] = self.ELBOW_90[j]

        #-------------------create list of percentages-----------------

        for i in range(len(self.temp)):
            for j in range(len(self.MAX_STRGHT)):
                self.perc[i][j] = self.temp[i][j] / self.MAX_STRGHT[j]

        #-------------------calculation loop---------------------------
        # not working correct needs lots of work!!
        # first loop works but need to modify so it can account for bust

    def calculate(self, idx_comp=0, idx_pipe=0):

        temp_count = 0

        while True:
            if idx_pipe == 0 and (self.temp[idx_comp][0] + self.total_lgt) <= self.MAX_STRGHT[0] and self.perc[idx_comp][0] + self.total_perc <= 1:
                self.total_lgt += self.temp[idx_comp][0]
                self.total_perc += self.perc[idx_comp][0]
                self.pipe_size_list.append(0)
                idx_comp += 1
                temp_count += 1
                if temp_count == len(self.temp):
                    break

            elif idx_pipe > 0 and (self.temp[idx_comp][1] + self.total_lgt) <= self.MAX_STRGHT[1] and self.perc[idx_comp][1] + self.total_perc <= 1:
                self.total_lgt += self.temp[idx_comp][1]
                self.total_perc += self.perc[idx_comp][1]
                self.pipe_size_list.append(1)
                idx_comp += 1
                temp_count += 1
                if temp_count == len(self.temp):
                    break

            elif idx_pipe > 0 and (self.temp[idx_comp][2] + self.total_lgt) <= self.MAX_STRGHT[2] and self.perc[idx_comp][2] + self.total_perc <= 1:
                self.total_lgt += self.temp[idx_comp][2]
                self.total_perc += self.perc[idx_comp][2]
                self.pipe_size_list.append(2)
                idx_comp += 1
                temp_count += 1
                if temp_count == len(self.temp):
                    break

            else:
                self.pipe_size_list = []
                self.total_lgt = 0
                self.total_perc = 0
                idx_pipe += 1
                self.calculate(0, idx_pipe)
                break

        # return round(total_lgt), idx_list, (round(total_perc * 100, 2))

    def bellows(self):
        pass
    '''if total length of the vent pipe exceeds 30 feet a bellows (expansion joint) is required to allow for contraction and movement of the pipe.'''


#-----------------------------------------------------------


if __name__ == "__main__":
    # execute only if run as a script (see GUI for app)
    main()


# temp for testing
# print(quench_run.comp_list)
# print(quench_run.strght_list)


# Hitachi notes below
'''THE CUSTOMERS ARCHITECT / ENGINEER IS RESPONSIBLE FOR UTILIZING THE FOLLOWING INFORMATION TO CALCULATE AND DESIGN THE CRYOGEN VENT LINE.

1) CALCULATE THE TOTAL APPARENT LENGTH OF THE QUENCH VENT.  START THE    CALCULATION ASSUMING A SMOOTH ELBOW (SEE TABLE 2) AND 4” ID PIPE. A. L1 + E1 + (L2 + L3) = LA (26’-0”) + (3’-9” (FROM TABLE 2)) + (12’-0”) = 41’-10”

2) APPARENT LENGTH (LA) = 41’-10”.  FROM TABLE 1, 6” ID PIPE IS REQUIRED.

3) PIPE SIZES MAY BE MIXED. A. THE PERCENTAGE OF ACTUAL TO ALLOWABLE LENGTH FOR EACH DIAMETER      OF PIPE MUST BE CALCULATED. B. THE COMBINED TOTAL OF PERCENTAGES MUST NOT EXCEED 100%. C. WHEN CHANGING PIPE SIZES, A DIFFUSER IS REQUIRED (SEE DIFFUSER SIZING    DIAGRAM THIS PAGE). D. THE LENGTH OF THE DIFFUSER IS INCLUDED IN THE LENGTH OF THE SMALLER    DIAMETER PIPE TO WHICH IT IS ATTACHED.
4
) FROM THE MAXIMUM PERMISSIBLE LENGTH CHART, THE ALLOWABLE LENGTH OF 4”    PIPE IS 18’. A. THE 8’ SECTION SHOWN IN THE ADJACENT DIAGRAM ACCOUNTS FOR    8/18 = 44.44% OF THIS ALLOWABLE LENGTH.

5) THE REMAINING LENGTH OF 6” PIPE MUST BE LESS THAN 55.56% OF THE ALLOWABLE 6” LENGTH. A. 77’ X 55.56% (.5556) = 42’-9”.

6)  THE APPARENT LENGTH OF 6” PIPE IS: A. L1 + E1 + L2  =LA     (26’-0”) + (5’-8” (FROM TABLE 2)) + (4’-0”) = 35’-7” B. THIS IS LESS THAN THE ALLOWED 42’-9” (55.56% OF 77’) OF 6” PIPE SO THE VENT PIPE AS SHOWN IN THE DIAGRAM IS ACCEPTABLE.

7) THE TOTAL LENGTH OF THE VENT PIPE EXCEEDS 30’; THEREFORE A BELLOWS    (EXPANSION JOINT) SECTION IS REQUIRED TO ALLOW FOR CONTRACTION AND    MOVEMENT OF THE PIPE. A. THE MAXIMUM LENGTH OF A BELLOWS SECTION MUST BE LESS THAN 2% OF    THE ALLOWABLE PIPE LENGTH. B. IN THE EXAMPLE ABOVE MAXIMUM LENGTH IS 8’-0” + 42’-9” = 50’-9” C. 50’-9” (609”) X .02 = 12

'''

''' Test case

1 = 200
2
3
1 = 725
2
3
1 = 120 '''
