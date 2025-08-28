class Vehicle:
    """Base class for all vehicles"""
    
    def __init__(self, brand, model, year, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.is_moving = False
    
    def start_engine(self):
        """Start the vehicle's engine"""
        print(f"{self.brand} {self.model}'s engine is starting... 🚀")
        return True
    
    def stop_engine(self):
        """Stop the vehicle's engine"""
        print(f"{self.brand} {self.model}'s engine is stopping... ⛔")
        self.is_moving = False
        return True
    
    def move(self):
        """Base move method - will be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement move() method")
    
    def get_info(self):
        """Get vehicle information"""
        return f"{self.year} {self.color} {self.brand} {self.model}"
    
    def __str__(self):
        return self.get_info()


class Car(Vehicle):
    """Car class inheriting from Vehicle"""
    
    def __init__(self, brand, model, year, color, doors, fuel_type):
        super().__init__(brand, model, year, color)
        self.doors = doors
        self.fuel_type = fuel_type
        self.wheels = 4
    
    def move(self):
        """Car-specific move implementation"""
        if self.start_engine():
            self.is_moving = True
            print(f"{self.brand} {self.model} is driving on the road! 🚗💨")
            return "Driving"
        return "Failed to move"
    
    def honk(self):
        """Car-specific method"""
        print("Honk! Honk! 🚗📯")
    
    def get_info(self):
        base_info = super().get_info()
        return f"{base_info} | {self.doors} doors | {self.fuel_type} fuel"


class Airplane(Vehicle):
    """Airplane class inheriting from Vehicle"""
    
    def __init__(self, brand, model, year, color, wingspan, max_altitude):
        super().__init__(brand, model, year, color)
        self.wingspan = wingspan
        self.max_altitude = max_altitude
        self.is_flying = False
    
    def move(self):
        """Airplane-specific move implementation"""
        if self.start_engine():
            self.take_off()
            return "Flying"
        return "Failed to move"
    
    def take_off(self):
        """Airplane-specific method"""
        print(f"{self.brand} {self.model} is taking off! ✈️🛫")
        self.is_moving = True
        self.is_flying = True
        print("Flying at cruising altitude! ☁️")
    
    def land(self):
        """Airplane-specific method"""
        print(f"{self.brand} {self.model} is landing! 🛬")
        self.is_flying = False
        self.stop_engine()
    
    def get_info(self):
        base_info = super().get_info()
        return f"{base_info} | Wingspan: {self.wingspan}m | Max Altitude: {self.max_altitude}ft"


class Boat(Vehicle):
    """Boat class inheriting from Vehicle"""
    
    def __init__(self, brand, model, year, color, length, max_speed_knots):
        super().__init__(brand, model, year, color)
        self.length = length
        self.max_speed_knots = max_speed_knots
        self.is_docked = True
    
    def move(self):
        """Boat-specific move implementation"""
        if self.start_engine():
            self.is_docked = False
            self.is_moving = True
            print(f"{self.brand} {self.model} is sailing on the water! ⛵🌊")
            return "Sailing"
        return "Failed to move"
    
    def dock(self):
        """Boat-specific method"""
        print(f"{self.brand} {self.model} is docking! 🚢⚓")
        self.is_docked = True
        self.stop_engine()
    
    def get_info(self):
        base_info = super().get_info()
        return f"{base_info} | Length: {self.length}m | Max Speed: {self.max_speed_knots} knots"


class Bicycle(Vehicle):
    """Bicycle class inheriting from Vehicle"""
    
    def __init__(self, brand, model, year, color, gears, bike_type):
        super().__init__(brand, model, year, color)
        self.gears = gears
        self.bike_type = bike_type
        self.wheels = 2
    
    def start_engine(self):
        """Override - bicycles don't have engines!"""
        print("Pedaling to start moving! 🚴‍♂️")
        return True
    
    def stop_engine(self):
        """Override - bicycles don't have engines!"""
        print("Applying brakes to stop! 🛑")
        self.is_moving = False
        return True
    
    def move(self):
        """Bicycle-specific move implementation"""
        self.is_moving = True
        print(f"{self.brand} {self.model} is pedaling on the road! 🚴‍♂️💨")
        return "Pedaling"
    
    def ring_bell(self):
        """Bicycle-specific method"""
        print("Ring! Ring! 🔔")


# Activity 2: Polymorphism Challenge! 🎭
def test_polymorphism():
    """Demonstrate polymorphism with different vehicle types"""
    
    # Create different types of vehicles
    vehicles = [
        Car("Toyota", "Camry", 2022, "Blue", 4, "Gasoline"),
        Airplane("Boeing", "737", 2018, "White", 35.8, 41000),
        Boat("Yamaha", "242X", 2021, "Red", 7.3, 45),
        Bicycle("Trek", "FX 2", 2023, "Black", 21, "Hybrid")
    ]
    
    print("🚗 VEHICLE POLYMORPHISM DEMONSTRATION 🚗")
    print("=" * 50)
    
    # Test the polymorphic move() method
    for i, vehicle in enumerate(vehicles, 1):
        print(f"\n{i}. {vehicle.get_info()}")
        print("-" * 30)
        
        # This is where polymorphism shines!
        movement_type = vehicle.move()
        print(f"Movement type: {movement_type}")
        
        # Stop the vehicle
        vehicle.stop_engine()
        print()


# Additional demonstration
def create_vehicle_showroom():
    """Create and display various vehicles"""
    
    print("🏎️ VEHICLE SHOWROOM 🏎️")
    print("=" * 40)
    
    # Create specific vehicle instances
    my_car = Car("Honda", "Civic", 2023, "Silver", 4, "Hybrid")
    my_plane = Airplane("Airbus", "A320", 2020, "Blue", 35.8, 39000)
    my_boat = Boat("Bayliner", "VR5", 2022, "White", 5.5, 38)
    my_bike = Bicycle("Specialized", "Sirrus", 2023, "Green", 18, "City")
    
    # Display vehicle information
    vehicles = [my_car, my_plane, my_boat, my_bike]
    
    for vehicle in vehicles:
        print(f"\n{vehicle}")
        print(f"Type: {vehicle.__class__.__name__}")
        
        # Test movement
        vehicle.move()
        vehicle.stop_engine()
        print()


# Run the demonstrations
if __name__ == "__main__":
    test_polymorphism()
    print("\n" + "="*60 + "\n")
    create_vehicle_showroom()