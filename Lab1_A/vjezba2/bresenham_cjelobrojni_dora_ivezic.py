from pyglet.gl import *
import pyglet


width = 500
height = 500
title = "Bresenhamov algoritam - crtanje linije"
window = pyglet.window.Window(width, height, title)

x1 = y1 = x2 = y2 = None

print("Kliknite misem na zaslon za postaviti tocku.")
print("Za brisanje ekrana pritisnite tipku C. \n")


# key press event   
@window.event
def on_key_press(symbol, modifier):
 
    # key "C" get press
    if symbol == pyglet.window.key.C:
         
        window.clear()
        print("Key C is pressed - clearing the window \n")

        global x1, y1, x2, y2

        x1 = y1 = x2 = y2 = None

        
 
# on mouse press event
@window.event
def on_mouse_press(x, y, button, modifiers):
    global x1, y1, x2, y2

    if x1 is None:
        x1 = x
        y1 = y
    elif x2 is None:
        x2 = x
        y2 = y

    window.clear()
    

    print("V1 = ",x1, y1)
    print("V2 = ",x2, y2)
    print()
    
    if x1 is not None and x2 is not None:
        LINE()

        BRESENHAM()


def LINE():
    global x1, y1, x2, y2

    glBegin(GL_LINES)
    glVertex2i(x1, y1+20)
    glVertex2i(x2, y2+20)
    glEnd()



def BRESENHAM():
    global x1, y1, x2, y2
    
    if x1<=x2:
        if y1 <= y2:
            bresenham_pozitivan_kut(x1,y1,x2,y2)
        else:
            bresenham_negativan_kut(x1,y1,x2,y2)
    else:
        if y1 >= y2:
            bresenham_pozitivan_kut(x2,y2,x1,y1)
        else:
            bresenham_negativan_kut(x2,y2,x1,y1)


def bresenham_pozitivan_kut(x1, y1, x2, y2):

    if y2-y1 <= x2-x1:
        a = 2 * (y2-y1)
        yc = y1
        yf = -(x2-x1)
        korekcija = 2 * yf  #korekcija = - 2 * (x2-x1)

        glBegin(GL_POINTS)
        for x in range( x1, x2+1 ):
            glVertex2i(x, yc)
            yf += a
            if yf >= 0:
                yf += korekcija
                yc += 1
        glEnd()

    else:
        #zamijeni x1 i y1
        x = x1
        x1 = y1
        y1 = x

        #zamijeni x2 i y2
        x = x2
        x2 = y2
        y2 = x

        yc = y1
        yf = -(x2-x1)
        korekcija = 2 * yf
        a = 2 * (y2-y1)

        glBegin(GL_POINTS)
        for x in range( x1, x2+1 ):
            glVertex2i(yc, x)
            yf += a
            if yf >= 0:
                yf += korekcija
                yc += 1
        glEnd()


def bresenham_negativan_kut(x1, y1, x2, y2):

    if -(y2-y1) <= x2-x1:
        a = 2 * (y2-y1)
        yc = y1
        yf = x2-x1
        korekcija = 2 * yf  #korekcija = 2 * (x2-x1)

        glBegin(GL_POINTS)
        for x in range( x1, x2+1 ):
            glVertex2i(x, yc)
            yf += a
            if yf <= 0:
                yf += korekcija
                yc -= 1
        glEnd()

    else:
        #zamijeni x1 i y2
        x = x1
        x1 = y2
        y2 = x

        #zamijeni x2 i y1
        x = x2
        x2 = y1
        y1 = x

        yc = y1
        yf = x2-x1
        korekcija = 2*yf
        a = 2 * (y2-y1)

        glBegin(GL_POINTS)
        for x in range( x1, x2+1 ):
            glVertex2i(yc, x)
            yf += a
            if yf <= 0:
                yf += korekcija
                yc -= 1
        glEnd()

        
              
# start running the application
pyglet.app.run()