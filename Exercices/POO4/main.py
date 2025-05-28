from Parallélépipède import Parallélépipède


def main():
    parallelepipede = Parallélépipède(3, 4, 5)
    
    print(parallelepipede)
    print(f"Surface: {parallelepipede.surface()}")
    print(f"Périmètre: {parallelepipede.perimeter()}")
    print(f"Volume: {parallelepipede.volume()}")
    
if __name__ == "__main__":
    main()