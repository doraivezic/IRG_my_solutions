from pyglet.gl import *
import pyglet
import numpy as np
import math


#C:\Users\17080\Documents\UTR Uvod u teoriju racunarstva\1.lab2020\IRG\Vjezba4\objekti\kocka.obj
#C:\Users\17080\Documents\UTR Uvod u teoriju racunarstva\1.lab2020\IRG\Vjezba4\objekti\kontrolni_poligon.obj

#UČITATI POLIGON - npr kocku

fileinput = input("Ime datoteke: ")
o = open(fileinput, "r")
lines = o.readlines()
o.close()

#učitati vrhove i poligone
vrhovi = []
poligoni = []
for line in lines:
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



#UČITATI KONTROLNE TOČKE - tj očišta

fileinput = input("Ime datoteke: ")
o = open(fileinput, "r")
lines = o.readlines()
o.close()

kontrolni_poligon_vrhovi = []
for line in lines:
    kontrolni_poligon_vrhovi.append( list(map(int, line.split())) ) 


#MIJENJATI PARAMETAR t OD 0 DO 1, S KORAKOM 0.01
#ZA SVAKI t ODREDITI KOORDINATE x(t), y(t), z(t)
#ISCRTATI TOČKE

o = []
for t in np.arange(0, 1, 0.01):

    x,y,z = 0,0,0

    n = len(kontrolni_poligon_vrhovi) -1
    for i in range(n+1):
        b = math.factorial(n) / (math.factorial(i) * math.factorial(n-i))  * (round(t,2) ** i) * ((1-round(t,2)) ** (n-i)) 

        x += b * kontrolni_poligon_vrhovi[i][0]
        y += b * kontrolni_poligon_vrhovi[i][1]
        z += b * kontrolni_poligon_vrhovi[i][2]
    
    o.append([x,y,z])



N = len(o)
trenutno_ociste = 0
Glediste = [0,0,0]  #moramo imati i viewup vektor zato sto je glediste u ishodistu
viewup = [0,0,1]



#kao u vjezbi 5
def transformacije(Ociste):

    #ISTO RADIMO I ZA OČIŠTE I GLEDIŠTE ali ne spremamo u njih
    V = np.ones((1, 4))

    V[:,:-1] = np.array([Ociste])
    Ociste_novi = np.dot( V, np.dot(T, S)) [:,:-1] .tolist()[0]

    V[:,:-1] = np.array([Glediste])
    Glediste_novi = np.dot( V, np.dot(T, S)) [:,:-1] .tolist()[0]



    #MATRICA PROJEKCIJE P
    
    H = np.linalg.norm(np.array([Glediste[0] - Ociste[0], Glediste[1] - Ociste[1], Glediste[2] - Ociste[2]]))  #= math.sqrt( (Ociste[0]-Glediste[0])**2 + (Ociste[1]-Glediste[1])**2 + (Ociste[2]-Glediste[2])**2 )
    matrica_P = np.array([[1., 0., 0., 0.],
                        [0., 1., 0., 0.],
                        [0., 0., 0. ,1/H],
                        [0., 0., 0., 0.]])

    

    #MATRICA TRANSFORMACIJE POGLEDA T

    T1 = np.array([[1.,0.,0.,0.],
                [0.,1.,0.,0.],
                [0.,0.,1.,0.],
                [-Ociste_novi[0], -Ociste_novi[1], -Ociste_novi[2], 1.]])

    Tz = np.array([[1, 0, 0, 0], 
                [0, 1, 0, 0], 
                [0, 0, -1, 0], 
                [0, 0, 0, 1]])

    z = np.array( [Glediste[0] - Ociste[0], Glediste[1] - Ociste[1], Glediste[2] - Ociste[2]]) / H

    ViewUp = viewup.copy()
    ViewUp = np.array(ViewUp) / np.linalg.norm(np.array(ViewUp))
    x = np.cross(z, ViewUp)  # X = Z x ViewUP
    y = np.cross(x, z)       # y = X x z

    R = np.array([[x[0], y[0], z[0], 0], 
                    [x[1], y[1], z[1], 0], 
                    [x[2], y[2], z[2], 0], 
                    [0, 0, 0, 1]])
    matrica_T = T1 @ R @ Tz

    

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






width = 500
height = 500
title = "Vjezba6"
window = pyglet.window.Window(width, height, title)

glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

def update_frames(value):  #value je stvarno vrijeme
    global trenutno_ociste
    trenutno_ociste += 1
    if trenutno_ociste >= N:
        trenutno_ociste = 0
    on_draw()
    return


@window.event
def on_draw():

    window.clear()

    ociste_promatranja = o[trenutno_ociste]
    ociste_promatranja = transformacije(ociste_promatranja)


    #sada u ociste_promatranja imamo vrhove poligona, ali gledani iz očišta

    skaliranje = min(height, width)*0.2
    
    #ISCRTATI POLIGON

    for p in poligoni:
        glBegin(GL_TRIANGLES)  #PRIJE: GL_LINE_LOOP
        # 1 trokut
        for i in range(0,3):
            vrh = ociste_promatranja [p[i]-1] # 1 vrh
            glVertex3f(vrh[0]*skaliranje + width/2 , vrh[1]*skaliranje + width/2 , 0)
        glEnd()



pyglet.clock.schedule_interval(update_frames, 0.05)
        
# start running the application
pyglet.app.run()