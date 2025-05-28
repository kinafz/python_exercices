from Rectangle import Rectangle

class Parallélépipède(Rectangle):
    def __init__(self, longueur: float, largeur: float, hauteur: float):
        super().__init__(longueur, largeur)
        self.hauteur = hauteur

    def surface(self) -> float:
        return 2 * (super().surface() + self.longueur * self.hauteur + self.largeur * self.hauteur)
    
    def perimeter(self) -> float:
        return 4 * (self.longueur + self.largeur + self.hauteur)
    
    def volume(self) -> float:
        return super().surface() * self.hauteur

    def __str__(self) -> str:
        return f"Parallélépipède de dimensions {self.longueur} x {self.largeur} x {self.hauteur} avec un volume de {self.volume()}"