from pyglet.gl import *
import pyglet


width = 500
height = 500
title = "Crtanje poligona"
window = pyglet.window.Window(width, height, title)

n = []
N=0

a = []
b = []
c = []

# key press event   
@window.event
def on_key_press(symbol, modifier):
    global n, N, a, b, c
 
    # key "C" get pressed
    if symbol == pyglet.window.key.C:
         
        window.clear()
        print("\nKey C is pressed - insert new size to clear the window \n")

        n = []
        N = 0
        a = []
        b = []
        c = []

        while N<3:
            N = int(input("Upisite broj vrhova poligona (min 3): "))


 
# on mouse press event
@window.event
def on_mouse_press(x, y, button, modifiers):
    global n

    print(x, y)

    #window.clear()

    if N==0:
        return

    if len(n) < N-1:
        n.append((x,y))
        window.clear()

    elif len(n) == N-1:
        n.append((x,y))
        poligon()

    else:
        ispitaj_tocku(x,y)
        oboji()


def poligon():
    global a, b, c

    a.clear()
    b.clear()
    c.clear()

    window.clear()

    glBegin(GL_LINES)
    for i in range(0, len(n)):
        glVertex2i(n[i][0], n[i][1])
        if i == len(n)-1:
            glVertex2i(n[0][0], n[0][1])

            a.append( n[i][1] - n[0][1] )  #a(i) = y(i)  - y(i+1)
            b.append( -n[i][0] + n[0][0] )  #b(i) = -x(i) + x(i+1)
            c.append( n[i][0] * n[0][1] - n[0][0] * n[i][1] )  #c(i) = x(i) * y(i+1) - x(i+1) + y(i)

        else:
            glVertex2i(n[i+1][0], n[i+1][1])  

            a.append( n[i][1] - n[i+1][1] )  #a(i) = y(i)  - y(i+1)
            b.append( -n[i][0] + n[i+1][0] )  #b(i) = -x(i) + x(i+1)
            c.append( n[i][0] * n[i+1][1] - n[i+1][0] * n[i][1] ) #c(i) = x(i) * y(i+1) - x(i+1) + y(i)

    glEnd()

    return

def ispitaj_tocku(x,y):

    for i in range(len(a)):
        if x * a[i] + y * b[i] + c[i] > 0:
            print("Točka V je izvan poligona.")
            return
    print("Točka V je unutar poligona.")
    return


def y_min_max():
    y=[]
    for el in n:
        y.append(el[1])
    return min(y), max(y)

def oboji():
    xmin, xmax = min(n)[0], max(n)[0]
    ymin, ymax = y_min_max()

    window.clear()

    for y in range(ymin, ymax+1):
        L = xmin
        D = xmax

        for i in range(len(n)):
            if a[i]!=0:
                x = ( -b[i] * y - c[i]) / a[i]
                
                if i==len(n)-1:

                    if n[i][1]<n[0][1] and x>L:
                        L = x

                    if n[i][1]>=n[0][1] and x<D:
                        D = x

                else:

                    if n[i][1]<n[i+1][1] and x>L:
                        L = x

                    if n[i][1]>=n[i+1][1] and x<D:
                        D = x
            
        if L<D:
            glBegin(GL_LINES)
            glVertex2i( int(L), y)
            glVertex2i( int(D), y)
            glEnd()


    return





while N<3:
    N = int(input("Upisite broj vrhova poligona (min 3): "))
print("Kliknite misem na zaslon za postaviti tocke. Unesite ih u smjeru kazaljke na satu.")
print("Za brisanje ekrana pritisnite tipku C. \n")


# start running the application
pyglet.app.run()