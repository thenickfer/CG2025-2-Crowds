class Pessoa():
    def __init__(self, w, h):
        self.pos = Ponto(0, 0)     # Posição do canto inferior esquerdo
        self.w = w                 # Largura
        self.h = h                 # Altura
        self.c = (0, 1, 1)         # Cor inicial 
        self.list = []
        self.visible = False

class Ponto:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def print(self) -> None:
        print("Ponto (", self.x, ",", self.y, ")")

    def set(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # Soma de dois pontos
    def __add__(self, other):
        return Ponto(self.x + other.x, self.y + other.y)

    # Subtração entre pontos
    def __sub__(self, other):
        return Ponto(self.x - other.x, self.y - other.y)

    # Multiplicação por escalar
    def __mul__(self, escalar: float):
        return Ponto(self.x * escalar, self.y * escalar)