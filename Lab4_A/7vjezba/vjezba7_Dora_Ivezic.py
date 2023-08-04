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
Glediste = list(map(float, lines[1].rstrip().split() )) 

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





def normalaa(v1, v2, v3):
    A = ( v2[1]-v1[1] ) * ( v3[2]-v1[2] ) - ( v2[2]-v1[2] ) * ( v3[1]-v1[1] ) 
    B = -(v2[0]-v1[0])  * ( v3[2]-v1[2] ) + ( v2[2]-v1[2] ) * ( v3[0]-v1[0] ) 
    C = ( v2[0]-v1[0] ) * ( v3[1]-v1[1] ) - ( v2[1]-v1[1] ) * ( v3[0]-v1[0] ) 
    # D = ( -v1[0]*A[-1] - v1[1]*B[-1] - v1[2]*C[-1] )

    return A,B,C


#ODREDITI STRAŽNJE POLIGONE NA TIJELU
def back_polig(p):

    v1 = vrhovi [p[0]-1] # 1 vrh
    v2 = vrhovi [p[1]-1] # 2 vrh
    v3 = vrhovi [p[2]-1] # 3 vrh

    A,B,C = normalaa( v1, v2, v3 )
    normala = np.array([ A, B, C ])

    g_o = np.array([ Ociste[0]-Glediste[0], Ociste[1]-Glediste[1], Ociste[2]-Glediste[2] ])

    if g_o @ normala <=0:
        return True  # taj poligon je straznji poligon
    return False  #poligon je vidljiv (nije straznji)



#--------------
# ZA GOURAUDOVO SJENCANJE NAM TREBAJU NORMALE IZ SVAKOG VRHA
#ODREDITI NORMALE U VRHOVIMA T.D. NAĐEMO PROSJEK NORMALA POLIGONA KOJI IMAJU TAJ VRH

normale_poligona = []

for p in poligoni:  #SVI POLIGONI - I VIDLJIVI I NEVIDLJIVI

    v1 = vrhovi[ p[0]-1 ]
    v2 = vrhovi[ p[1]-1 ]
    v3 = vrhovi[ p[2]-1 ]

    A,B,C = normalaa( v1, v2, v3 )
    normala = np.array([ A, B, C ])
    normala = normala / np.linalg.norm(normala)

    normale_poligona.append( normala )



#UPAMITI KOJI VRH JE NA KOJIM POLIGONIMA

vrhovi_povrsine = x = [[] for i in range(len(vrhovi_T_P))]
for i in range(len(poligoni)):

    vrhovi_povrsine[poligoni[i][0]-1].append(i)
    vrhovi_povrsine[poligoni[i][1]-1].append(i)
    vrhovi_povrsine[poligoni[i][2]-1].append(i)

for el in vrhovi_povrsine:
    el = list(set(el)) 



#--------------
# za konstantno sjencanje TREBAMO ZNATI KOJI SU POLIGNI VIDLJIVI
vidljivi_poligoni = []
for p in poligoni:
    if back_polig(p):   #ako je p straznji poligon onda ga preskoci
        continue
    vidljivi_poligoni.append(p)
#poligoni = vidljivi_poligoni NE SMIJEMO PROMIJENITI POCETNU VARIJABLU

vidljivi_poligoni_indexi = []
for p in range(len(poligoni)):
    if back_polig(poligoni[p]):   #ako je p straznji poligon onda ga preskoci
        continue
    vidljivi_poligoni_indexi.append(p)




zadatak = 1

#za zad 2 i 3
Ia = 100  # intenzitet koji želimo (0-255)
ka = 0.4  # koef
Ii = 120  # intenzitet točkastog izvora svjetlosti
kd = 0.7  # empirijski koef refleksije



intenziteti = []

def konstantno_sjencanje():
    global intenziteti

    #ZADATI POLOŽAJ IZVORA
    izvor = input("Upiši položaj izvora svjetlosti: ")
    izvor = list(map(float, izvor.rstrip().split() ))

    #transformiraj izvor svjetla
    V[:,:-1] = np.array([izvor])
    izvor = np.dot( V, np.dot(T, S)) [:,:-1] .tolist()[0]


    #ODREDITI INTENZITETE (VIDLJIVIH) POLIGONA

    intenziteti.clear()

    L = np.array([ izvor[0]-x_avg, izvor[1]-y_avg, izvor[2]-z_avg ]) #vektor iz sredista poligona do izvora
    L = L / np.linalg.norm(L)

    for p in vidljivi_poligoni:

        v1 = vrhovi [p[0]-1] # 1 vrh
        v2 = vrhovi [p[1]-1] # 2 vrh
        v3 = vrhovi [p[2]-1] # 3 vrh

        A,B,C = normalaa( v1, v2, v3 )
        normala = np.array([ A, B, C ])
        normala = normala / np.linalg.norm(normala)

        #ambijentna komponenta
        Ig = Ia * ka    # intenzitet koji želimo (0-255) * koeficijent

        #difuzna komponenta
        Id = Ii * kd * ( max(0, L @ normala ) ) # intenzitet točkastog izvora * empirijski koef refleksije * kut

        intenziteti.append( Ig + Id )

    return


def Gouraud_sjencanje():
    global intenziteti

    intenziteti.clear()

    #ZADATI POLOŽAJ IZVORA
    izvor = input("Upiši položaj izvora svjetlosti: ")
    izvor = list(map(float, izvor.rstrip().split() ))

    #transformiraj izvor svjetla
    V[:,:-1] = np.array([izvor])
    izvor = np.dot( V, np.dot(T, S)) [:,:-1] .tolist()[0]



    #ODREDITI NORMALE U VRHOVIMA T.D. NAĐEMO PROSJEK NORMALA POLIGONA KOJI IMAJU TAJ VRH

    #ODREDITI INTENZITETE U VRHOVIMA pomocu normala vrhova

    #vrhovi_gour = []


    for i in range(len(vrhovi_T_P)) :

        L = np.array([ izvor[0]-vrhovi[i][0], izvor[1]-vrhovi[i][1], izvor[2]-vrhovi[i][2] ]) #vektor iz sredista poligona do izvora
        L = L / np.linalg.norm(L)

        suma_normala = 0
        for povrsina in vrhovi_povrsine[i]:
            suma_normala += normale_poligona[povrsina]

        normala_vrha = suma_normala / len(vrhovi_povrsine[i])

        #ambijentna komponenta
        Ig = Ia * ka    # intenzitet koji želimo (0-255) * koeficijent

        #difuzna komponenta
        Id = Ii * kd * ( max(0, L @ normala_vrha ) ) # intenzitet točkastog izvora * empirijski koef refleksije * kut

        #vrhovi_gour.append(i)
        intenziteti.append( Ig + Id )

    return







width = 500
height = 500
title = "Sjencanje"
window = pyglet.window.Window(width, height, title)


# key press event   
@window.event
def on_key_press(symbol, modifier):
    global zadatak

    if symbol == pyglet.window.key.A:
        konstantno_sjencanje()
        zadatak = 2

    elif symbol == pyglet.window.key.B:
        Gouraud_sjencanje()
        zadatak = 3

    elif symbol == pyglet.window.key.R: # r kao reset
        zadatak = 1



@window.event
def on_draw():

    window.clear()


    # # PRIKAZ TIJELA KORISTEĆI GLUT
    # gluPerspective(60, float(width/height), 0.2, 12)
    # gluLookAt(-Ociste[0], -Ociste[1], -Ociste[2], Glediste[0], Glediste[1], Glediste[2], 0., 1., 0.)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # if zadatak == 1:
    #     for p in vidljivi_poligoni:
    #         glColor3ub(70, 150, 120)
    #         glBegin(GL_LINE_LOOP)
    #         # 1 trokut
    #         for i in range(0,3):
    #             vrh = vrhovi [p[i]-1] # 1 vrh
    #             glVertex3f(vrh[0],vrh[1],vrh[2])
    #         glEnd()
    # return


    skaliranje = min(height, width)*2

    vrhovi_print  = []
    for el in vrhovi_T_P:
        vrhovi_print.append(list(el))

    for v in vrhovi_print:
        v[2] = 0
        v[0] = int(v[0]*skaliranje + width/2 ) #skaliranje i translacija 2 u 1
        v[1] = int(v[1]*skaliranje + height/2 )

    #ISCRTATI POLIGON

    if zadatak == 1:
        for p in vidljivi_poligoni:
            glColor3ub(70, 150, 120)
            glBegin(GL_LINE_LOOP)
            # 1 trokut
            for i in range(0,3):
                vrh = vrhovi_print [p[i]-1] # 1 vrh
                glVertex3f(vrh[0],vrh[1],vrh[2])
            glEnd()

    elif zadatak == 2:
        count = 0
        for p in vidljivi_poligoni:
            glColor3ub(70, int(round(intenziteti[count])), 120)
            count += 1
            glBegin(GL_TRIANGLES)
            # 1 trokut
            for i in range(0,3):
                vrh = vrhovi_print [p[i]-1] # 1 vrh
                glVertex3f(vrh[0],vrh[1],vrh[2])
            glEnd()

    elif zadatak == 3:
        for p in vidljivi_poligoni_indexi:
            glBegin(GL_TRIANGLES)
            # 1 trokut
            for i in range(0,3):
                vrh = vrhovi_print [poligoni[p][i]-1] # 1 vrh
                intenzitet = intenziteti [poligoni[p][i]-1] # 1 vrh
                glColor3ub(70, int(round(intenzitet)), 120)
                glVertex3f(vrh[0],vrh[1],vrh[2])
            glEnd()

    return
    

        
# start running the application
pyglet.app.run()