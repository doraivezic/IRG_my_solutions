from pyglet.gl import *
import pyglet
import numpy as np
import math

#C:\Users\17080\Documents\UTR Uvod u teoriju racunarstva\1.lab2020\IRG\Vjezba4\objekti\kocka.obj


fileinput = input("Ime datoteke: ")
o = open(fileinput, "r")
lines = o.readlines()
o.close()


#UČITANI POLIGON STAVLJAMO U SREDINU I SKALIRAMO NA -1,1

Ociste = list(map(int, lines[0].rstrip().split() ))
Glediste = list(map(int, lines[1].rstrip().split() )) 
#ako glediste odgovara ishodistu scene onda moramo dodati i ViewUp vektor kod računanja rotacijske matrice 
#pretpostavljamo da ne odgovara ishodistu scene, nego recimo sredistu tijela da si olaskamo zivot

#učitati vrhove i poligone
vrhovi = []
poligoni = []
for line in lines[2:]:
    if line[0]=='v':
        vrhovi.append( list(map(float, line[1:].split())) )  #svaki vrh uvijek ima 3 koordinate
    elif line[0]=='f':
        poligoni.append( list(map(int, line[1:].split())) )  #svaki poligon uvijek ima 3 vrha - trokut

#odrediti min i max koordinate
xmin, ymin, zmin = (min(idx) for idx in zip(*vrhovi))
xmax, ymax, zmax = (max(idx) for idx in zip(*vrhovi))

#odrediti središte tijela
x_avg = (xmin+xmax)/2
y_avg = (ymin+ymax)/2
z_avg = (zmin+zmax)/2

max_all = max(xmax-xmin, ymax-ymin, zmax-zmin) 

#postaviti u ishodiste i skalirati na raspon -1,1
T = np.array([[1.,0.,0.,0.],
              [0.,1.,0.,0.],
              [0.,0.,1.,0.],
              [-x_avg,-y_avg,-z_avg,1.]])
S = np.array([[2/max_all,0.,0.,0.],
              [0.,2/max_all,0.,0.],
              [0.,0.,2/max_all,0.],
              [0.,0.,0.,1]])
#matrica vrhova ali dodajem jos jedan stupac jedinica
a = np.array(vrhovi)
V = np.ones((len(vrhovi), 4))
V[:,:-1] = a

#V * T * S   ali bez zadnjeg reda
new_vertices = np.dot( V, np.dot(T, S)) [:,:-1]
vrhovi = []
vrhovi = new_vertices.tolist()



def f(Ociste, Glediste):


    #ISTO RADIMO I ZA OČIŠTE I GLEDIŠTE ali ne spremamo u njih
    V = np.ones((1, 4))

    V[:,:-1] = np.array([Ociste])
    Ociste_novi = np.dot( V, np.dot(T, S)) [:,:-1] .tolist()[0]

    V[:,:-1] = np.array([Glediste])
    Glediste_novi = np.dot( V, np.dot(T, S)) [:,:-1] .tolist()[0]

    
    
    #MATRICA TRANSFORMACIJE POGLEDA T

    T1 = np.array([[1.,0.,0.,0.],
                [0.,1.,0.,0.],
                [0.,0.,1.,0.],
                [-Ociste_novi[0], -Ociste_novi[1], -Ociste_novi[2], 1.]])

    Glediste1 = [Glediste_novi[0], Glediste_novi[1], Glediste_novi[2], 1] @ T1  #ili ovako ili direktno ubacitii vrijednosti prema formulama

    nazivnik = math.sqrt(Glediste1[0]**2 + Glediste1[1]**2)
    sin_a = Glediste1[1] / nazivnik          #kut alpha oko z osi
    cos_a = Glediste1[0] / nazivnik
    
    T2 = np.array([[cos_a, -sin_a, 0., 0.],
                [sin_a, cos_a, 0., 0.],
                [0., 0., 1. ,0.],
                [0., 0., 0., 1.]])

    Glediste2 = Glediste1@T2
    
    nazivnik = math.sqrt(Glediste2[0]**2 + Glediste2[2]**2)
    sin_b = Glediste2[0] / nazivnik     
    cos_b = Glediste2[2] / nazivnik

    T3 = np.array([[cos_b, 0., sin_b, 0.],
                [0., 1., 0., 0.],
                [-sin_b, 0., cos_b ,0.],
                [0., 0., 0., 1.]])

    Glediste3 = np.dot(Glediste2, T3)
    
    T4 = np.array([[0., -1., 0., 0.],
                [1., 0., 0., 0.],
                [0., 0., 1. ,0.],
                [0., 0., 0., 1.]])

    T5 = np.array([[-1., 0., 0., 0.],
                [0., 1., 0., 0.],
                [0., 0., 1. ,0.],
                [0., 0., 0., 1.]])

    matrica_T = T1 @ T2 @ T3 @ T4 @ T5



    #MATRICA PERSPEKTIVNE PROJEKCIJE P
    H = Glediste3[2]  #= math.sqrt( (Ociste[0]-Glediste[0])**2 + (Ociste[1]-Glediste[1])**2 + (Ociste[2]-Glediste[2])**2 )
    matrica_P = np.array([[1., 0., 0., 0.],
                        [0., 1., 0., 0.],
                        [0., 0., 0. ,1/H],
                        [0., 0., 0., 0.]])


    #NAPRAVI TRANSFORMACIJU I PROJEKCIJU VRHOVA POLIGONA
    vrhovi_T_P = []
    for v in vrhovi.copy():
        if len(v)<matrica_T.shape[0]:
            v.append(1.0)
        tmp = (v @ matrica_T @ matrica_P) .tolist()
        if tmp[3]>0 and not tmp[3]==1:
            tmp[0] = tmp[0] / tmp[3] /H
            tmp[1] = tmp[1] / tmp[3] /H
            tmp[2] = tmp[2] / tmp[3] /H
        vrhovi_T_P.append(tmp[:-1])

    return vrhovi_T_P


vrhovi_T_P = f(Ociste, Glediste)





width = 500
height = 500
title = "Projekcija"
window = pyglet.window.Window(width, height, title)


# key press event   
@window.event
def on_key_press(symbol, modifier):
    global Ociste, Glediste, vrhovi_T_P

    #ociste +: xyz
    #ociste -: abc

    #glediste +: efg
    #glediste -: ijk
 
    da = True

    if symbol == pyglet.window.key.X:
        Ociste[0] += 1
    elif symbol == pyglet.window.key.A:
        Ociste[0] -= 1
    elif symbol == pyglet.window.key.E:
        Glediste[0] += 1
    elif symbol == pyglet.window.key.I:
        Glediste[0] -= 1

    elif symbol == pyglet.window.key.Y:
        Ociste[1] += 1
    elif symbol == pyglet.window.key.B:
        Ociste[1] -= 1

    elif symbol == pyglet.window.key.F:
        Glediste[1] += 1
    elif symbol == pyglet.window.key.J:
        Glediste[1] -= 1

    elif symbol == pyglet.window.key.Z:
        Ociste[2] += 1
    elif symbol == pyglet.window.key.C:
        Ociste[2] -= 1

    elif symbol == pyglet.window.key.G:
        Glediste[2] += 1
    elif symbol == pyglet.window.key.K:
        Glediste[2] -= 1

    else:
        da = False

    if da:
        #izracunaj nove vrijednosti vrhova, automatski ce se i refreshat slika jer se poziva on_draw()
        vrhovi_T_P = f(Ociste, Glediste)


@window.event
def on_draw():

    window.clear()

    skaliranje = min(height, width)*2
    for v in vrhovi_T_P:
        v[2] = 0
        v[0] = int(v[0]*skaliranje + width/2 ) #skaliranje i translacija 2 u 1
        v[1] = int(v[1]*skaliranje + height/2 )

    #ISCRTATI POLIGON

    for p in poligoni:
        glBegin(GL_LINE_LOOP)
        # 1 trokut
        for i in range(0,3):
            vrh = vrhovi_T_P [p[i]-1] # 1 vrh
            glVertex3f(vrh[0],vrh[1],vrh[2])
        glEnd()
        
# start running the application
pyglet.app.run()