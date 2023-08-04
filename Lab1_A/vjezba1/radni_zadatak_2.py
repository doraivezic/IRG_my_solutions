import numpy as np

def main():

    equation_system = []
    right_side = []
    for i in range(3):
        equation = []
        for j in range(3):
            equation.append( int(input("Unesite %d. vrijednost u %d. jednadzbi: " %(j+1, i+1))) )
        equation_system.append(equation)

        right_side.append( int(input("Unesite 4. vrijednost u %d. jednadzbi: " %(i+1))) )


    solution = np.linalg.solve( np.array(equation_system), np.array(right_side) )
    print("[x,y,z] =", solution)
    solution = np.dot ( np.linalg.inv(np.array(equation_system)), np.array(right_side).T )
    print("[x,y,z] =", solution)

    return

if __name__ == "__main__":
    main()