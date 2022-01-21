class Soil:
    '''
    Класс Soil используется для получения значения 
    удельного электрического споротивления грунта
    '''
    def __init__(self, soil_resistance):
            self.soil_resistance = soil_resistance

    def get_soil_resistance(self):
        '''Возвращает значение удельного электрического споротивления грунта'''
        return self.soil_resistance