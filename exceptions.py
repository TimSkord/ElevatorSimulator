class InvalidFloorError(Exception):
    def __init__(self, chosen_floor, min_floor, max_floor):
        self.chosen_floor = chosen_floor
        self.min_floor = min_floor
        self.max_floor = max_floor
        message = f"The chosen floor {chosen_floor} is out of the valid range ({min_floor}-{max_floor})."
        super().__init__(message)


class ElevatorOverloadedError(Exception):
    def __init__(self, capacity, passenger_count):
        self.capacity = capacity
        self.passenger_count = passenger_count
        message = (f"The elevator was overloaded. Expected capacity {capacity}, "
                   f"actual number of passengers {passenger_count}.")
        super().__init__(message)
