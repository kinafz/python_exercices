class WaterTank:
    total_water_volume = 0.0
    
    def __init__(self, weight: float, capacity: float, current_level: float):
        self.weight = weight
        self.capacity = capacity
        self.current_level = current_level
        WaterTank.total_water_volume += current_level

    def fill(self, amount: float):
        if amount < 0:
            raise ValueError("Amount to fill must be positive.")
        WaterTank.total_water_volume -= self.current_level
        self.current_level += amount
        if self.current_level > self.capacity:
            self.current_level = self.capacity

        WaterTank.total_water_volume += self.current_level

    def drain(self, amount: float):
        if amount < 0:
            raise ValueError("Amount to drain must be positive.")
        old_level = self.current_level
        self.current_level -= amount
        if self.current_level < 0:
            self.current_level = 0.0
        WaterTank.total_water_volume -= old_level - self.current_level

    def get_current_level(self) -> float:
        return self.current_level

    def get_capacity(self) -> float:
        return self.capacity