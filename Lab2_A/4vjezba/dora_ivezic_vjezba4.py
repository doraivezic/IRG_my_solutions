from pyglet.gl import *
import pyglet
import numpy as np

#C:\Users\17080\Documents\UTR Uvod u teoriju racunarstva\1.lab2020\IRG\Vjezba4\objekti\tetrahedron.obj


fileinput = input("Ime datoteke: ")
o = open(fileinput, "r")
lines = o.readlines()
o.close()

#izborjiti broj vrhova i poligona
br_vrhova = 0
br_poligona = 0
for line in lines:
    if line[0]=='v':
        br_vrhova += 1 
    elif line[0]=='f':
        br_poligona += 1 

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


#učitati koordinate ispitne točke
V = list(map(float, input("Koordinate ispitne točke V: ").split() ))

A = []
B = []
C = []
D = []
for p in poligoni:
    v1 = vrhovi[ p[0] -1]
    v2 = vrhovi[ p[1] -1]
    v3 = vrhovi[ p[2] -1]
    A.append( ( v2[1]-v1[1] ) * ( v3[2]-v1[2] ) - ( v2[2]-v1[2] ) * ( v3[1]-v1[1] ) )
    B.append( -(v2[0]-v1[0])  * ( v3[2]-v1[2] ) + ( v2[2]-v1[2] ) * ( v3[0]-v1[0] ) )
    C.append( ( v2[0]-v1[0] ) * ( v3[1]-v1[1] ) - ( v2[1]-v1[1] ) * ( v3[0]-v1[0] ) )
    D.append( -v1[0]*A[-1] - v1[1]*B[-1] - v1[2]*C[-1] )



unutar_tijela = True
for i in range(len(A)):
    if A[i]*V[0] + B[i]*V[1] + C[i]*V[2] + D[i] > 0:
        unutar_tijela = False
        print("V je izvan tijela.")
        #sad znamo da poligon nije konveksan
        #povlacimo zraku iz tocke i ako se siječe sa tijelom 
        # u neparanom broju sjecista onda je unutar tijela i tijelo je konkavno
        #ray tracing
        #ali to se ne trazi u zadatku
        break

if unutar_tijela:
    print("V je unutar tijela.")
    






width = 500
height = 500
title = "Crtanje tijela"
window = pyglet.window.Window(width, height, title)

@window.event
def on_draw():

    skaliranje = min(height, width)*0.4
    for v in vrhovi:
        v[2] = 0
        v[0] = int(v[0]*skaliranje + width/2 ) #skaliranje i translacija 2 u 1
        v[1] = int(v[1]*skaliranje + height/2 )


    
    for p in poligoni:
        glBegin(GL_LINE_LOOP)
        # 1 trokut
        for i in range(0,3):
            vrh = vrhovi[p[i]-1] # 1 vrh
            glVertex3f(vrh[0],vrh[1],vrh[2])
        glEnd()
        
# start running the application
pyglet.app.run()

