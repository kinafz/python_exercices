class Rectangle:
    def __init__(self, longueur, largeur):
        self.longueur = longueur
        self.largeur = largeur

    def surface(self):
        return self.longueur * self.largeur

    def perimeter(self):
        return 2 * (self.longueur + self.largeur)

    def __str__(self):
        return f"Rectangle(longueur={self.longueur}, largeur={self.largeur})"