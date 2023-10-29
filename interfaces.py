from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .elevator import Elevator


class ElevatorInterface(ABC):

    @abstractmethod
    def __init__(self, capacity=4, top_floor=10):
        """
        self.lower_floor - Number of the lowest floor of the building
        self.top_floor - Number of floors in the building
        self.capacity - Elevator capacity, determined during initialization
        self.doors_open - True if the doors are open
        self.current_floor - Current floor, default lower_floor
        self.direction - Direction of elevator movement
        self.queue - The number of floors to which the elevator was called
        self.passengers - Passenger object list
        """

    @abstractmethod
    def add_floor_to_queue(self, floor: int) -> None:
        """Adds a floor to the elevator service queue."""
        pass

    def remove_floor_from_queue(self, floor: int) -> None:
        """Removes from the queue the floor on which the elevator has already stopped."""

    @abstractmethod
    def move(self) -> None:
        """Performs the movement of the elevator to the next floor in the queue."""
        pass

    @abstractmethod
    def open_doors(self) -> None:
        """Opens the elevator doors."""
        pass

    @abstractmethod
    def close_doors(self) -> None:
        """Closes the elevator doors."""
        pass

    @abstractmethod
    def choose_direction(self) -> None:
        """Determines the direction of elevator movement by analyzing who
         called the elevator where and when."""
        pass


class PassengerInterface(ABC):

    def __init__(self, current_floor: int, target_floor: int):
        """
        self.current_floor = floor from which the passenger calls the elevator
        self.target_floor = floor to which the passenger calls the elevator
        """

    def call_elevator(self, elevator: 'Elevator') -> None:
        """Adds a floor to the elevator floor queue"""
        pass

    def enter_the_elevator(self, elevator: 'Elevator') -> None:
        """A passenger enters the elevator"""
        pass

    def select_floor(self, elevator: 'Elevator') -> None:
        """The passenger selects a floor, if the floor has already been selected
         - nothing happens."""
        pass
