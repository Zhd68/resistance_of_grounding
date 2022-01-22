import soil

class HorizontalGroundingElectrode:
    '''
    Класс VerticalGroundingElectrode используется для получения значения
    сопротивления растеканию тока одиночного горизонтального заземлителя
    длиной 5 метров 
    '''

    LENGHT_OF_BELT = int(5)
    
    def __init__(self, depth_of_laying, width_of_belt, hight_of_belt):
        self.__depth_of_laying = depth_of_laying
        self.__width_of_belt = width_of_belt
        self.__hight_of_belt = hight_of_belt
        self.__soil_resistance = None

    def add_soil(self, soil_resistance):
        '''Добавляет удельное электрическое споротивление грунта'''
        self.__soil_resistance = soil.Soil(soil_resistance).get_soil_resistance()

    def __equivalent_diameter(self):
        '''Возвращает эквивалентный диаметр стальной полосы'''
        return (self.__width_of_belt * self.__hight_of_belt) ** (0.5)

    def resistance_h_electrode(self):
        '''Возвращает сопротивление растеканию тока одиночного горизонтального заземлителя'''
        from math import pi, log, sqrt
        resistance = (self.__soil_resistance / (2 * pi * self.LENGHT_OF_BELT)) * \
            (log(2 * self.LENGHT_OF_BELT / self.__equivalent_diameter()) \
                + log((self.LENGHT_OF_BELT + sqrt(self.LENGHT_OF_BELT ** 2 \
                    + 16 * self.__depth_of_laying ** 2)) / (4 * self.__depth_of_laying)))
        return resistance


class VerticalGroundingElectrode:
    '''
    Класс VerticalGroundingElectrode используется для получения значения
    сопротивления растеканию тока одиночного вертикального заземлителя
    длиной 4.5 метров 
    '''

    LENGHT_OF_ROD = float(4.5)
    
    def __init__(self, depth_of_rod, diameter_of_rod):
        #глубина указывается от поверхности до центра стержня
        self.__depth_of_rod = depth_of_rod
        self.__diameter_of_rod = diameter_of_rod
        self.__soil_resistance = None

    def add_soil(self, soil_resistance):
        '''Добавляет удельное электрическое споротивление грунта'''
        self.__soil_resistance = soil.Soil(soil_resistance).get_soil_resistance()

    def resistance_v_electrode(self):
        '''Возвращает сопротивление растеканию тока одиночного вертикального заземлителя'''
        from math import pi, log
        resistance = (self.__soil_resistance / (2 * pi * self.LENGHT_OF_ROD)) * \
            (log(2 * self.LENGHT_OF_ROD / self.__diameter_of_rod) \
                + 0.5 * log((4 * self.__depth_of_rod + self.LENGHT_OF_ROD) \
                    / (4 * self.__depth_of_rod - self.LENGHT_OF_ROD)))
        return resistance

class GroundingDevice:
    '''
    Класс GroundingDevice используется для получения значения
    сопротивления растеканию тока заземляющего устройства, состоящего
    из вретикальных стержней (длиной 4.5 м) соединенных между собой
    горизонтальной полосой (длиной 5 метров)
    '''

    def __init__(self, number_of_v_electrodes):
        self.__number_of_v_electrodes = number_of_v_electrodes
        self.__horizontal_electrode = None
        self.__vertical_electrode = None

    def add_horizontal_electrode(self, depth_of_laying, width_of_belt, hight_of_belt, soil_resistance):
        '''Добавляет единичный горизонтальный заземлитель'''
        self.__horizontal_electrode = HorizontalGroundingElectrode(depth_of_laying, width_of_belt, hight_of_belt)
        self.__horizontal_electrode.add_soil(soil_resistance)

    def add_vertical_electrode(self, depth_of_rod, diameter_of_rod, soil_resistance):
        '''Добавляет единичный вертикальный заземлитель'''
        self.__vertical_electrode = VerticalGroundingElectrode(depth_of_rod, diameter_of_rod)
        self.__vertical_electrode.add_soil(soil_resistance)

    def __shielding_horizontal_electrode(self):
        '''
        Возвращяет коэффициент экранирования горизонтальных заземлителей.
        Формула получена степенной аппроксимацией справочных данных.
        '''
        return 0.9695 * (self.__number_of_v_electrodes ** (-0.171))

    def __shielding_vertical_electrode(self):
        '''
        Возвращяет коэффициент экранирования вертикальных заземлителей.
        Формула получена степенной аппроксимацией справочных данных.
        '''
        return 1.0952 * (self.__number_of_v_electrodes ** (-0.294))

    def __resistance_all_h_electrode(self):
        '''Возвращает сопротивление растеканию тока горизонтальных заземлителей (с учетом экранирующего эффекта)'''
        return self.__horizontal_electrode.resistance_h_electrode() \
            / ((self.__number_of_v_electrodes - 1) * self.__shielding_horizontal_electrode())

    def __resistance_all_v_electrode(self):
        '''Возвращает сопротивление растеканию тока вертикальных заземлителей (с учетом экранирующего эффекта)'''
        return self.__vertical_electrode.resistance_v_electrode() \
            / (self.__number_of_v_electrodes * self.__shielding_vertical_electrode())

    def resistance_grounding_device(self):
        '''Возвращает полное сопротивление растеканию тока заземляющего устройства'''
        return (self.__resistance_all_v_electrode() * self.__resistance_all_h_electrode()) \
            / (self.__resistance_all_v_electrode() + self.__resistance_all_h_electrode())