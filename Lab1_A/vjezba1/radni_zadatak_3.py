import numpy as np

def P(a,b,c):
    return np.linalg.norm( np.cross( (b-a), (c-a) ) ) #izostavljeno dijeljenje s 2 jer se ionako pokrati

def main():

    trokut = [[0,0,0],[0,0,0],[0,0,0]]  #x1x2x3, y1y2y3, z1z2z3
    for i in range(3):
        for j in range(3):
            trokut[j][i] = int(input("%d. vrh, %d. koordinata: " %(i+1, j+1)))
        
    tockaT = []
    for j in range(3):
        tockaT.append( int(input("Tocka T, %d. koordinata: " %(j+1))) )


    tockaT = np.array(tockaT)

    

    try:
        trokut = np.array(trokut)
        #solution = np.linalg.solve( trokut, tockaT )
        solution = np.dot ( np.linalg.inv( trokut ), tockaT.T )
    except:
        #ne postoji inverz matrice trokuta

        #računanje baricentričnih koordinata preko omjera površina

        a = np.array(trokut[0])
        b = np.array(trokut[1])
        c = np.array(trokut[2])

        povrsina_total = P(a,b,c)
        
        t1 = P(tockaT, b, c) / povrsina_total
        t2 = P(tockaT, a, c) / povrsina_total
        t3 = P(tockaT, a, b) / povrsina_total
        
        solution = np.array([t1,t2, t3])

    
    print("Baricentrične koordinate točke T s obzirom na zadani trokut:", solution)

    return

if __name__ == "__main__":
    main()