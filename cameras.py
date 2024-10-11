class Camera:
    def __init__(self, id, ip, usuario, clave, in1, out1, in2, out2):
        self.id = id
        self.ip = ip
        self.usuario = usuario
        self.clave = clave
        self.in1 = in1
        self.in2 = in2
        self.out1 = out1
        self.out2 = out2

    def __str__(self):
        return f'IP:{self.ip}- Entrada:{self.in1}-{self.in2}-{self.out1}-{self.out2}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.ip == other.ip

    def to_sql_insert(self):
        return f'INSERT into registros (camara_id, in1, out1, in2, out2) VALUES (\'{self.id}\', \'{self.in1}\', \'{self.out1}\', \'{self.in2}\', \'{self.out2}\')'