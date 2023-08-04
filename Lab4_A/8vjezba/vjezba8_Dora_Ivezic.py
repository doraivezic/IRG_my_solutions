import math
from pyglet.gl import *


eps = float(input("Upiši epsilon: "))

m = int(input("Upiši maksimalan broj iteracija: "))

umin, umax, vmin, vmax = tuple(map(float, input("Upiši područje kompleksne ravnine: ").rstrip().split() ))

c = complex(input("Upiši kompleksnu konstantu c: ")) #0.32+0.043j


# eps=100
# m=16

# umin = -1.0
# umax = 1.0
# vmin = -1.2
# vmax = 1.2

# c=complex(0.32,0.043)




def Mendelbrot():

    #ZA SVAKU TOČKU ZASLONA RADITI POSTUPAK ZA MENDELBROTOV SKUP
    glBegin(GL_POINTS)
    for x0 in range(xmax):
        for y0 in range(ymax):

            u0 = (umax-umin)/xmax * x0 + umin
            v0 = (vmax-vmin)/ymax * y0 + vmin
            c = complex( u0,v0 )

            k = -1.0
            z = complex( 0,0 )
            r = 0.0

            while r < eps and k < m:

                k = k + 1 
                z = z*z + c

                r = math.sqrt( z.real**2 + z.imag**2  )

            if r < eps:
                glColor3f( 0,0,0 ) #divergencija nije utvrđena
            else:
                glColor3f( k/m,  1.0 - k/m /2,  0.8 - k/m /3)  #utvrđena je divergencija u koraku k


            # if k>=m: #ovako nedostaje zadnja iteracija
            #     glColor3f( 0,0,0 ) #divergencija nije utvrđena
            # else:
            #     glColor3f( k/m,  1.0 - k/m /2,  0.8 - k/m /3)  #utvrđena je divergencija u koraku k
            #     #glColor3f( 1.,1.,1.)

            glVertex2i(x0,y0)
    glEnd()


def Julije():
    #ZA SVAKU TOČKU ZASLONA RADITI POSTUPAK ZA JULIJEV SKUP
    glBegin(GL_POINTS)
    for x0 in range(xmax):
        for y0 in range(ymax):

            #c je globalno ucitan

            u0 = (umax-umin)/xmax * x0 + umin
            v0 = (vmax-vmin)/ymax * y0 + vmin
            z = complex( u0,v0 )
            
            k = -1.0
            r = 0

            while r < eps and k < m:

                k = k + 1 
                z = z*z + c

                r = math.sqrt( z.real**2 + z.imag**2  )

            if r < eps:
                glColor3f( 0,0,0 ) #divergencija nije utvrđena
            else:
                glColor3f( k/m,  1.0 - k/m /2,  0.8 - k/m /3)  #utvrđena je divergencija u koraku k

            glVertex2i(x0,y0)
    glEnd()




width = 300
height = 200
title = "Fraktali"
window = pyglet.window.Window(width, height, title)

#PROČITATI RAZLUČIVOST ZASLONA
xmax = width
ymax = height

prvi_zadatak = True

@window.event
def on_key_press(symbol, modifier):
    global prvi_zadatak
    if symbol == pyglet.window.key.M:
        prvi_zadatak = True
    elif symbol == pyglet.window.key.J:
        prvi_zadatak = False

@window.event
def on_draw():
    window.clear()

    if prvi_zadatak:
        Mendelbrot()
    else:
        Julije()
    
pyglet.app.run()