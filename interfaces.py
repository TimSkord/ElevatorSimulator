from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .elevator import Elevator


class ElevatorInterface(ABC):
    """
    Represents an elevator system.

    Attributes:
        lower_floor (int): The lowest floor the elevator can reach.
        top_floor (int): The highest floor the elevator can reach.
        capacity (int): The maximum number of passengers the elevator can carry.
        doors_open (bool): Indicates if the elevator doors are open.
        _current_floor (int): The floor where the elevator currently is.
        direction (str or None): The direction in which the elevator is moving. Can be 'up', 'down' or None.
        queue (set): A set of floors the elevator intends to visit.
        passengers (set): A set of passengers currently in the elevator.
        directions (dict): Dictionary mapping directions to methods.
    """

    @abstractmethod
    def add_floor_to_queue(self, floor: int) -> None:
        """Adds a floor to the elevator service queue."""

    def remove_floor_from_queue(self, floor: int) -> None:
        """Removes from the queue the floor on which the elevator has already stopped."""

    @abstractmethod
    def move(self) -> None:
        """Performs the movement of the elevator to the next floor in the queue."""

    @abstractmethod
    def open_doors(self) -> None:
        """Opens the elevator doors."""

    @abstractmethod
    def close_doors(self) -> None:
        """Closes the elevator doors."""

    @abstractmethod
    def choose_direction(self) -> None:
        """Determines the direction of elevator movement by analyzing who
         called the elevator where and when."""


class PassengerInterface(ABC):
    @abstractmethod
    def __init__(self, current_floor: int, target_floor: int):
        """
        self.current_floor = floor from which the passenger calls the elevator
        self.target_floor = floor to which the passenger calls the elevator
        """

    @abstractmethod
    def set_elevator(self, elevator: 'Elevator'):
        """Sets the Elevator for the passenger"""

    @abstractmethod
    def call_elevator(self) -> None:
        """Adds a floor to the elevator floor queue"""

    @abstractmethod
    def enter_the_elevator(self) -> None:
        """A passenger enters the elevator"""

    @abstractmethod
    def select_floor(self) -> None:
        """The passenger selects a floor, if the floor has already been selected
         - nothing happens."""
