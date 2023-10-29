from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .elevator import Elevator


class ElevatorInterface(ABC):

    @abstractmethod
    def __init__(self, capacity=4, top_floor=10):
        '''
        self.state = elevator state, can be 'idle', 'moving_up', 'moving_down'
        self.doors_open = True if the doors are open
        self.current_floor = current floor, default 1
        self.top_floor = number of floors in the building
        self.queue = the number of floors to which the elevator was called
        self.capacity = elevator capacity, determined during initialization
        self.passengers = passenger object list
        '''

    @abstractmethod
    def add_floor_to_queue(self, floor: int) -> None:
        '''Adds a floor to the elevator service queue.'''
        pass

    @abstractmethod
    def move(self) -> None:
        '''Performs the movement of the elevator to the next floor in the queue.'''
        pass

    @abstractmethod
    def open_doors(self) -> None:
        '''Opens the elevator doors.'''
        pass

    @abstractmethod
    def close_doors(self) -> None:
        '''Closes the elevator doors.'''
        pass

    @abstractmethod
    def choose_direction(self) -> None:
        '''Determines the direction of elevator movement by analyzing who
         called the elevator where and when.'''
        pass


class PassengerInterface(ABC):

    def __init__(self, current_floor: int, target_floor: int):
        '''
        self.current_floor = floor from which the passenger calls the elevator
        self.target_floor = floor to which the passenger calls the elevator
        '''

    def call_elevator(self, elevator: 'Elevator') -> None:
        '''Adds a floor to the elevator floor queue'''
        pass

    def enter_the_elevator(self, elevator: 'Elevator') -> None:
        '''A passenger enters the elevator'''
        pass

    def select_floor(self, elevator: 'Elevator') -> None:
        '''The passenger selects a floor, if the floor has already been selected
         - nothing happens.'''
        pass

    def get_out_of_the_elevator(self, elevator: 'Elevator') -> None:
        '''Passenger leaving the elevator'''
        pass
