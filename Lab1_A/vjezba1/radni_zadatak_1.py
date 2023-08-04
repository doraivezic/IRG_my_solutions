import numpy as np

def main():

    v1 = np.array([2, 3, -4]) + np.array([-1, 4, -1])
    print("v1 =", v1)
    
    #skalarni produkt tj suma produkata pojedinih komponenti
    s = np.dot(v1, np.array([-1, 4, -1]))
    print("s =", s)

    #vektorski produkt
    v2 = np.cross(v1, np.array([2, 2, 4]))
    print("v2 =", v2)

    #normirani vektor - normalize a vector to its corresponding unit vector
    v3 = v2 / np.linalg.norm(v2)
    print("v3 =", v3)

    v4 = - v2
    print("v4 =", v4)


    matrix1 = np.array([[1,2,3], [2,1,3], [4,5,1]])
    matrix2 = np.array([[-1,2,-3], [5,-2,7], [-4,-1,3]])

    #zbrajanje matrica
    M1 = matrix1 + matrix2
    print("M1:\n", M1)

    #skalarno mnozenje matrica -- uz transponiranje druge matrice
    M2 = np.dot(matrix1, matrix2.T)
    print("M2:\n", M2)

    #skalarno mnozenje matrica -- uz inverz druge matrice
    M3 = np.dot(matrix1, np.linalg.inv(matrix2))
    print("M3:\n", M3)

    return

if __name__ == "__main__":
    main()