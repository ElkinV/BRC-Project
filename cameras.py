class Camera:
    def __init__(self, id, ip, usuario, clave, in1, in2, out1, out2):
        self.id = id
        self.ip = ip
        self.usuario = usuario
        self.clave = clave
        self.in1 = in1
        self.in2 = in2
        self.out1 = out1
        self.out2 = out2

    def __str__(self):
        return f'{self.ip}-{self.regla_1}-{self.in_1}-{self.regla_2}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.ip == other.ip

