class HorizontalGroundingElectrode:
    '''
    Класс VerticalGroundingElectrodes используется для получения значения
    сопротивления растеканию тока одиночного горизонтального заземлителя
    длиной 5 метров 
    '''

    LENGHT_OF_BELT = int(5)
    
    def __init__(self, depth_of_laying, width_of_belt, hight_of_belt):
        self.depth_of_laying = depth_of_laying
        self.width_of_belt = width_of_belt
        self.hight_of_belt = hight_of_belt
        self.soil_resistance = None

    def add_soil(self, soil_resistance):
        '''Добавляет удельное электрическое споротивление грунта'''
        self.soil_resistance = soil.Soil(soil_resistance).get_soil_resistance()

    def equivalent_diameter(self):
        '''Возвращает эквивалентный диаметр стальной полосы'''
        return (self.width_of_belt * self.hight_of_belt) ** (0.5)

    def resistance_h_electrode(self):
        '''Сопротивление растеканию тока одиночного горизонтального заземлителя'''
        from math import pi, log, sqrt
        resistance = (self.soil_resistance / (2 * pi * self.LENGHT_OF_BELT)) * \
            (log(2 * self.LENGHT_OF_BELT / self.equivalent_diameter()) \
                + log((self.LENGHT_OF_BELT + sqrt(self.LENGHT_OF_BELT ** 2 \
                    + 16 * self.depth_of_laying ** 2)) / (4 * self.depth_of_laying)))
        return resistance


class VerticalGroundingElectrode:
    pass

class GroundingDevice:
    pass