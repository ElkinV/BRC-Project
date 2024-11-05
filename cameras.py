class Camera:
    def __init__(self, id=None,ip=None, usuario=None, clave=None, in1=0, out1=0, in2=0, out2=0):
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
            return self.in1 == other.in1 and self.in2 == other.in2 and self.out1 == other.out1 and self.out2 == other.out2

    def to_sql_insert(self):
        return f'INSERT into registros (camara_id, in1, out1, in2, out2) VALUES (\'{self.id}\', \'{self.in1}\', \'{self.out1}\', \'{self.in2}\', \'{self.out2}\')'