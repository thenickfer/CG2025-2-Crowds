import colorsys
import math
import time

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from Quadtree import Quadtree
from models import Pessoa, Ponto
# Classe que representa um ponto 2D com operações básicas

    
class Frame:
    def __init__(self, x: float, y: float, f: int):
        self.x = x
        self.y = y
        self.f = f

    def set(self, x: float, y: float, f: int) -> None:
        self.x = x
        self.y = y
        self.f = f

# Classe que representa um quadrado desenhável

# Lista de quadrados (inicia com um)
pessoas = []
num_quadrado = 0  # Índice do quadrado atual

tempo_antes = time.time()
soma_dt = 0

# Variáveis de controle da câmera
left = 0
right = 0
top = 0
bottom = 0
panX = 0
panY = 0

# Desenha os eixos X e Y no mundo (visuais)
def desenhaEixos():
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)
    glLineWidth(1)

    glBegin(GL_LINES)
    glVertex2f(left, 0)
    glVertex2f(right, 0)
    glVertex2f(0, bottom)
    glVertex2f(0, top)
    glEnd()

    glPopMatrix()

# Desenha um quadrado na posição (x, y), com tamanho (w, h)
def desenhaQuadrado(x, y, w, h):
    glPushMatrix()
    glLoadIdentity()  # <- Faltavam os parênteses aqui!

    glTranslatef(x, y, 0)

    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(w, 0)
    glVertex2f(w, h)
    glVertex2f(0, h)
    glEnd()

    glPopMatrix()

# Função principal de desenho da cena
def Desenha():
    global left, right, top, bottom, panX, panY

    # Define a área visível (viewport) com deslocamento (pan)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)

    # Limpa a tela com preto
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    # Desenha todos os quadrados
    for pessoa in pessoas:
        if pessoa.visible:
            glColor3f(*pessoa.c)
            desenhaQuadrado(pessoa.pos.x, pessoa.pos.y, pessoa.h, pessoa.w)

    # Desenha os eixos
    desenhaEixos()

    # Finaliza os comandos de desenho
    glFlush()

# Função para teclas do teclado comum (ASCII)
def Teclado(key: chr, x: int, y: int):
    global num_quadrado, panX, panY

    if key == 27:  # Tecla ESC
        exit(0)


    # Teclas WASD para mover a câmera (pan)
    if key == b'a':
        panX -= 0.01
    if key == b'd':
        panX += 0.01
    if key == b'w':
        panY += 0.01
    if key == b's':
        panY -= 0.01  
    # Solicita redesenho
    glutPostRedisplay()

# Função para teclas especiais (setas) — move o quadrado atual
def TeclasEspeciais(key: int, x: int, y: int):


    glutPostRedisplay()

# Inicializa as configurações do sistema de coordenadas
def Inicializa():
    global left, right, top, bottom, frame
    frame = 0

    

    with open("Paths_JP.txt") as file:
        firstLine = file.readline().strip().replace('[', '').replace(']', '').split(',')
        divisor = [float(firstLine[0]), float(firstLine[1])]
        for line in file:
            pes = Pessoa(0.01, 0.01)
            line = line.replace('(', ' ').replace(')', ' ')
            """ for char in range(len(line)):
                if line[char] == '(' or line[char] == ')':
                    line = line[:char] + ' ' + line[char+1:] """
            parts = line.split()
            parts.pop(0)
            parts.pop(0)
            for coord in parts: 
                coord = coord.split(',')
                pes.list.append(Frame(float(coord[0])/divisor[0], float(coord[1])/divisor[1], float(coord[2])))
            pessoas.append(pes)

            



    glMatrixMode(GL_PROJECTION)
    left = -1
    right = 1
    top = 1
    bottom = -1
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)


# Função de atualização para animação

quadTree =  Quadtree(1, 1, Ponto(0, 0), 10)

colors = [(0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]

def update():
    global pessoas, right, left, soma_dt, tempo_antes, frame

    tempo_agora = time.time()
    delta_time = tempo_agora - tempo_antes
    tempo_antes = tempo_agora
    soma_dt += delta_time
    if soma_dt > 1.0 / 30:  # Atualiza ~30 vezes por segundo
        soma_dt = 0
        frame+=1
        quadTree.clear()
        for pessoa in pessoas:
            quadTree.insert(pessoa)
        for pessoa in pessoas:
            if not pessoa.list:
                pessoa.visible = False
                continue
            fnumber = pessoa.list[0].f
            if(frame == fnumber):
                pessoa.visible = True
                newPos = pessoa.list.pop(0)
                pessoa.pos.x = newPos.x
                pessoa.pos.y = newPos.y  
                neighbors = quadTree.findBetween(pessoa.pos - Ponto(0.1, 0.1), pessoa.pos + Ponto(0.1, 0.1))
        
                closestDist = 1

                for neighbor in neighbors:
                    newDist = math.sqrt((neighbor.pos.x - pessoa.pos.x) ** 2 + (neighbor.pos.y - pessoa.pos.y) ** 2)
                    closestDist = min(closestDist, newDist)

                pessoa.c = colors[round(closestDist/0.02)%len(colors)]

        glutPostRedisplay()

# Função principal
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"Desenha OpenGL")

    glutDisplayFunc(Desenha)
    glutKeyboardFunc(Teclado)
    glutSpecialFunc(TeclasEspeciais)

    Inicializa()

    glutIdleFunc(update)

    try:
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()