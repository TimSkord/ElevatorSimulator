from random import choice, randint
from time import sleep
from typing import Optional

from constants import DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR, DEFAULT_CAPACITY, UP_NAME, DOWN_NAME
from exceptions import InvalidFloorError, ElevatorOverloadedError
from interfaces import ElevatorInterface, PassengerInterface
from utils import find_closest, has_larger, has_smaller, generate_full_name, set_elevator_for_passengers


class Elevator(ElevatorInterface):
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

    def __init__(self,
                 capacity: int = DEFAULT_CAPACITY,
                 lower_floor: int = DEFAULT_LOWER_FLOOR,
                 top_floor: int = DEFAULT_TOP_FLOOR) -> None:
        """Initializes the elevator with default or given parameters."""
        self.lower_floor = lower_floor
        self.top_floor = top_floor
        self.capacity = capacity
        self.doors_open = False
        self._current_floor = self.lower_floor
        self.direction = None
        self.queue = set()
        self.passengers = set()
        self.directions = {
            None: self.rest,
            UP_NAME: self.up_one_floor,
            DOWN_NAME: self.down_one_floor,
        }

    @property
    def state(self) -> str:
        """Returns the current state of the elevator, either moving in a direction or idle."""
        if self.direction:
            return f"move_{self.direction}"
        return 'idle'

    @property
    def current_floor(self) -> int:
        """Returns the current floor of the elevator."""
        return self._current_floor

    @current_floor.setter
    def current_floor(self, new_floor: int):
        """Sets the current floor of the elevator if the new floor is within range."""
        if self.lower_floor <= new_floor <= self.top_floor:
            self._current_floor = new_floor
        else:
            raise InvalidFloorError(new_floor, self.lower_floor, self.top_floor)

    @property
    def movement_permitted(self, raise_exception: bool = False) -> bool:
        """Determines if the elevator can move based on its passenger capacity."""
        overweight = len(self.passengers) <= self.capacity
        if raise_exception:
            raise ElevatorOverloadedError(self.capacity, len(self.passengers))
        return overweight

    def eject_random_passenger(self) -> None:
        """Ejects a random passenger from the elevator until the elevator is within capacity."""
        if self.movement_permitted:
            return
        self.getting_off()
        return self.eject_random_passenger()

    def add_floor_to_queue(self, *args: int) -> None:
        """Adds one or more floors to the elevator's queue."""
        self.queue.update(args)

    def remove_floor_from_queue(self, floor: int) -> None:
        """Removes a floor from the elevator's queue if present."""
        if floor in self.queue:
            self.queue.remove(floor)

    def open_doors(self):
        """Opens the elevator doors."""
        self.doors_open = True
        print("The door is open.")

    def close_doors(self):
        """Closes the elevator doors."""
        self.doors_open = False
        print("The door is closed.")

    def passengers_getting_off(self, passenger_list: set):
        """Handles the logic when passengers are getting off the elevator."""
        for passenger in passenger_list:
            self.getting_off(passenger)

    def getting_off(self, passenger=None):
        """Handles the logic when a passenger is getting off the elevator."""
        if passenger:
            self.passengers.remove(passenger)
            print(f"{passenger} leaves the elevator with his head held high with pride")
        else:
            passenger = self.passengers.pop()
            print(f"In an unequal fight, passenger {passenger} leaves the elevator.")
        passenger.got_off_the_elevator(self.current_floor)

    def passengers_entering(self, passenger):
        """Handles a passenger entering the elevator."""
        self.passengers.add(passenger)
        print(f"{passenger} stepped into the elevator as if it were his home.")

    def close_doors_if_open(self):
        """Checks the state of the doors and closes them if they are open."""
        if self.doors_open:
            self.close_doors()

    def stop_at_current_floor_if_needed(self):
        """Checks if the elevator needs to stop at the current floor."""
        if self.current_floor in self.queue:
            self.open_doors()

    def disembark_passengers_if_needed(self):
        """Checks if any passenger needs to get off at the current floor."""
        who_go_out = set()
        for passenger in self.passengers:
            if passenger.target_floor == self.current_floor:
                who_go_out.add(passenger)
        if who_go_out:
            self.passengers_getting_off(who_go_out)

    def choose_direction(self):
        """Determines the direction the elevator should move in based on the queue and current floor."""

        def determine_initial_direction(target_floor, current_floor):
            """Helper function to determine the direction towards the closest floor."""
            if target_floor > current_floor:
                return UP_NAME
            elif target_floor == current_floor:
                return None
            return DOWN_NAME

        sorted_queue = sorted(self.queue)
        closest_floor = find_closest(sorted_queue, self.current_floor)
        has_calls_above = has_larger(sorted_queue, self.current_floor)
        has_calls_below = has_smaller(sorted_queue, self.current_floor)

        # If there are no floors in the queue, the elevator remains idle.
        if not closest_floor:
            self.direction = None
            return

        # If the elevator is currently idle, set the direction towards the closest floor.
        if not self.direction:
            self.direction = determine_initial_direction(closest_floor, self.current_floor)
            return

        # If the elevator is currently going up, but there are no more calls above and there are calls below.
        if self.direction == UP_NAME and not has_calls_above and has_calls_below:
            self.direction = DOWN_NAME
            return

        # If the elevator is currently going down, but there are no more calls below and there are calls above.
        if self.direction == DOWN_NAME and not has_calls_below and has_calls_above:
            self.direction = UP_NAME

    def move(self) -> None:
        """Moves the elevator based on the current queue and passenger destinations."""
        if self.queue:
            self.eject_random_passenger()
            self.choose_direction()
            self.close_doors_if_open()
            self.directions[self.direction]()
            self.stop_at_current_floor_if_needed()
            self.disembark_passengers_if_needed()
            self.remove_floor_from_queue(self.current_floor)
        else:
            self.rest()

    def rest(self):
        """Handles the elevator logic when it's not moving."""
        self.direction = None
        self.close_doors_if_open()

    def up_one_floor(self):
        """Moves the elevator up by one floor."""
        self.current_floor += 1
        print(f"The elevator arrived on the {self.current_floor} floor.")

    def down_one_floor(self):
        """Moves the elevator down by one floor."""
        self.current_floor -= 1
        print(f"The elevator arrived on the {self.current_floor} floor.")

    def __str__(self) -> str:
        """Returns a string representation of the elevator's current status."""
        message = f"""
        Floor: {self.current_floor}
        Passengers: {list(self.passengers)}
        Directions: {self.direction}
        Queue: {sorted(self.queue)}
        State: {self.state}
        Doors open: {self.doors_open}
        """
        return message


class Passenger(PassengerInterface):
    """
    Represents a passenger in the elevator system.

    Attributes:
        name (str): Name of the passenger.
        current_floor (int): The current floor where the passenger is.
        target_floor (int): The target floor the passenger wants to go to.
        _is_resting (bool): Represents if the passenger is resting and not intending to move.
        _awaits (bool): Represents if the passenger is waiting for the elevator.
        _in_elevator (bool): Represents if the passenger is currently inside the elevator.
        _elevator (Optional[Elevator]): Reference to the elevator object.
    """

    def __init__(self, name: Optional[str] = None, current_floor: int = 1, target_floor: int = 9):
        """Initializes a new passenger."""
        self.name = name if name else generate_full_name()
        self.current_floor = current_floor
        self.target_floor = target_floor
        self._is_resting = True
        self._awaits = False
        self._in_elevator = False
        self._elevator = None

    def set_elevator(self, elevator: Elevator) -> None:
        """Set the elevator for the passenger."""
        self._elevator = elevator

    def call_elevator(self) -> None:
        """Call the elevator to the current floor of the passenger."""
        self._elevator.add_floor_to_queue(self.current_floor)
        self._awaits = True
        print(f"{self} called the elevator while on the {self.current_floor} floor.")

    def enter_the_elevator(self) -> None:
        """Logic for the passenger to enter the elevator."""
        if self._elevator.doors_open:
            self._elevator.passengers_entering(self)
            self._in_elevator = True

    def select_floor(self) -> None:
        """Logic for the passenger to select a floor inside the elevator."""
        if self._in_elevator:
            if self.target_floor not in range(self._elevator.lower_floor, self._elevator.top_floor + 1):
                raise InvalidFloorError(self.target_floor, self._elevator.lower_floor, self._elevator.top_floor)
            self._elevator.add_floor_to_queue(self.target_floor)
            print(f"{self} nervously presses the {self.target_floor}th floor button.")

    def set_a_new_target(self) -> None:
        """Set a new random target floor for the passenger."""
        possible_floors = [floor for floor in range(DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR + 1) if
                           floor != self.current_floor]
        new_floor = choice(possible_floors)
        self.target_floor = new_floor

    def got_off_the_elevator(self, new_floor: int) -> None:
        """Logic for the passenger to get off the elevator."""
        self.current_floor = new_floor
        self._is_resting = True
        self._awaits = False
        self._in_elevator = False

    def move(self) -> None:
        """
        Simulates the passenger's movement logic.
        Depending on the state, the passenger might move, call the elevator, or enter the elevator.
        """
        # If the passenger is already in the elevator, no further actions are needed.
        if self._in_elevator:
            return

        # If the passenger is resting, there's a chance they might decide to move.
        if self._is_resting:
            # Creates a 1 in 51 chance that a passenger will decide to move.
            # Which is the statistical chance of an elevator call per minute on a typical workday.
            if randint(0, 50) == 0:
                self._is_resting = False
                self.set_a_new_target()
            return

        # If the passenger is on the same floor as the elevator, they can enter and select a floor.
        if self.current_floor == self._elevator.current_floor:
            self.enter_the_elevator()
            self.select_floor()
            return

        # If the passenger is not awaiting the elevator, they can call it.
        if not self._awaits:
            self.call_elevator()

    def __repr__(self) -> str:
        return self.name


def generate_random_passengers(count: int) -> list:
    """Creates the specified number of random passengers"""
    passengers = []
    for i in range(count):
        passengers.append(Passenger(
            current_floor=randint(DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR),
            target_floor=randint(DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR)
        ))
    return passengers


def run_simulation():
    """Runs a simulation of elevator operation and passenger movements."""
    elevator = Elevator()
    passengers = generate_random_passengers(20)
    set_elevator_for_passengers(passengers, elevator)
    for _ in range(100):
        elevator.move()
        for passenger in passengers:
            passenger.move()
        print(elevator)
        sleep(1)  # TODO: Remove the string for instant execution
