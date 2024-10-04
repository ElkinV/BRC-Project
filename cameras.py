class Camera:
    def __init__(self, ip, regla_1, in_1, regla_2, in_2):
        self.ip = ip
        self.regla_1 = regla_1
        self.in_1 = in_1
        self.regla_2 = regla_2
        self.in_2 = in_2

    def __str__(self):
        return f'{self.ip}-{self.regla_1}-{self.in_1}-{self.regla_2}'

