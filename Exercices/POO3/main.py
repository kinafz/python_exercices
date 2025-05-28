import WaterTank

def main():
    tank1 = WaterTank.WaterTank(weight=10.0, capacity=100.0, current_level=50.0)

    print(f"[tank1] Initial fill level: {tank1.get_current_level()} liters")
    print(f"Total water volume: {WaterTank.WaterTank.total_water_volume} liters")

    tank1.fill(30.0)
    print(f"[tank1] Fill level after filling 30 liters: {tank1.get_current_level()} liters")
    print(f"Total water volume: {WaterTank.WaterTank.total_water_volume} liters")

    tank1.drain(20.0)
    print(f"[tank1] Fill level after draining 20 liters: {tank1.get_current_level()} liters")
    print(f"Total water volume: {WaterTank.WaterTank.total_water_volume} liters")
    
    tank2 = WaterTank.WaterTank(weight=10.0, capacity=90.0, current_level=25.0)

    print(f"[tank2] Initial fill level: {tank2.get_current_level()} liters")
    print(f"Total water volume: {WaterTank.WaterTank.total_water_volume} liters")

    tank2.fill(15.0)
    print(f"[tank2] Fill level after filling 30 liters: {tank2.get_current_level()} liters")
    print(f"Total water volume: {WaterTank.WaterTank.total_water_volume} liters")

    tank2.drain(5.0)
    print(f"[tank2] Fill level after draining 20 liters: {tank2.get_current_level()} liters")
    print(f"Total water volume: {WaterTank.WaterTank.total_water_volume} liters")
    
if __name__ == "__main__":
    main()