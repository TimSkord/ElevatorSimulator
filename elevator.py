from random import choice, randint
from time import sleep

from constants import DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR, DEFAULT_CAPACITY, UP_NAME, DOWN_NAME
from interfaces import ElevatorInterface, PassengerInterface
from utils import find_closest, has_larger, has_smaller, generate_full_name


class Elevator(ElevatorInterface):

    def __init__(self, capacity=DEFAULT_CAPACITY, lower_floor=DEFAULT_LOWER_FLOOR, top_floor=DEFAULT_TOP_FLOOR):
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
        if self.direction:
            return f"move_{self.direction}"
        return 'idle'

    @property
    def current_floor(self) -> int:
        return self._current_floor

    @current_floor.setter
    def current_floor(self, new_floor: int):
        if self.lower_floor <= new_floor <= self.top_floor:
            self._current_floor = new_floor

    @property
    def movement_permitted(self) -> bool:
        return len(self.passengers) <= self.capacity

    def to_push_a_random_person_out_of_an_elevator(self) -> None:
        if self.movement_permitted:
            return
        weakest_link = choice(list(self.passengers))
        self.passengers_getting_off({weakest_link})
        print(f"In an unequal fight, passenger {weakest_link} leaves the elevator.")
        return self.to_push_a_random_person_out_of_an_elevator()

    def add_floor_to_queue(self, *args: int) -> None:
        self.queue.update(args)

    def remove_floor_from_queue(self, floor: int) -> None:
        if floor in self.queue:
            self.queue.remove(floor)

    def open_doors(self):
        self.doors_open = True
        print("The door is open.")

    def close_doors(self):
        self.doors_open = False
        print("The door is closed.")

    def passengers_getting_off(self, passenger_list: set):
        for passenger in passenger_list:
            self.passengers.remove(passenger)
            passenger.got_off_the_elevator(self.current_floor)
            print(f"{passenger} leaves the elevator with his head held high with pride")

    def passengers_entering(self, passenger):
        self.passengers.add(passenger)
        print(f"{passenger} stepped into the elevator as if it were his home.")

    def check_doors(self):
        if self.doors_open:
            self.close_doors()

    def check_current_floor(self):
        if self.current_floor in self.queue:
            self.open_doors()

    def check_passengers(self):
        who_go_out = set()
        for passenger in self.passengers:
            if passenger.target_floor == self.current_floor:
                who_go_out.add(passenger)
        if who_go_out:
            self.passengers_getting_off(who_go_out)

    def choose_direction(self):
        sorted_queue = sorted(self.queue)
        closest_floor = find_closest(sorted_queue, self.current_floor)
        calls_above = has_larger(sorted_queue, self.current_floor)
        calls_below = has_smaller(sorted_queue, self.current_floor)

        if not closest_floor:
            self.direction = None
        elif not self.direction:
            if closest_floor > self.current_floor:
                self.direction = UP_NAME
            elif closest_floor < self.current_floor:
                self.direction = DOWN_NAME
        elif self.direction == UP_NAME and (not calls_above and calls_below):
            self.direction = DOWN_NAME
        elif self.direction == DOWN_NAME and (not calls_below and calls_above):
            self.direction = UP_NAME

    def move(self) -> None:
        if self.queue:
            self.to_push_a_random_person_out_of_an_elevator()
            self.choose_direction()
            self.check_doors()
            self.directions[self.direction]()
            self.check_current_floor()
            self.check_passengers()
            self.remove_floor_from_queue(self.current_floor)
        else:
            self.rest()

    def rest(self):
        self.direction = None
        self.check_doors()

    def up_one_floor(self):
        self.current_floor += 1
        print(f"The elevator arrived on the {self.current_floor} floor.")

    def down_one_floor(self):
        self.current_floor -= 1
        print(f"The elevator arrived on the {self.current_floor} floor.")

    def __str__(self) -> str:
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

    def __init__(self, name=None, current_floor=1, target_floor=9):
        self.name = name if name else generate_full_name()
        self.current_floor = current_floor
        self._target_floor = target_floor
        self.respite = True  # parameter to simulate human activity on the floor
        self.awaits = False
        self.in_elevator = False

    @property
    def target_floor(self) -> int:
        return self._target_floor

    @target_floor.setter
    def target_floor(self, new_floor: int):
        if new_floor != self.current_floor:
            self._target_floor = new_floor
        else:
            self.set_a_new_target()  # deliberate recursion

    def call_elevator(self, elevator: Elevator) -> None:
        elevator.add_floor_to_queue(self.current_floor)
        print(f"{self} called the elevator while on the {self.current_floor} floor.")
        self.awaits = True

    def enter_the_elevator(self, elevator: Elevator) -> None:
        if elevator.doors_open:
            elevator.passengers_entering(self)
            self.in_elevator = True

    def select_floor(self, elevator: Elevator) -> None:
        if self.in_elevator:
            elevator.add_floor_to_queue(self.target_floor)
            print(f"{self} nervously presses the {self.target_floor}th floor button.")

    def set_a_new_target(self):
        target_list = set(range(DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR + 1))
        target_list.remove(self.target_floor)
        new_target = choice(list(target_list))
        self.target_floor = new_target

    def got_off_the_elevator(self, new_floor: int):
        self.current_floor = new_floor
        self.respite = True
        self.awaits = False
        self.in_elevator = False

    def move(self, elevator: Elevator) -> None:
        if self.in_elevator:
            return
        elif self.respite:
            reluctance = randint(0, 50)
            if not reluctance:
                self.respite = False
                self.set_a_new_target()
        elif self.current_floor == elevator.current_floor:
            self.enter_the_elevator(elevator)
            self.select_floor(elevator)
        elif self.awaits:
            pass
        else:
            self.call_elevator(elevator)

    def __repr__(self) -> str:
        return self.name


def generate_random_passengers(count: int) -> list:
    passengers = []
    for i in range(count):
        passengers.append(Passenger(
            current_floor=randint(DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR),
            target_floor=randint(DEFAULT_LOWER_FLOOR, DEFAULT_TOP_FLOOR)
        ))
    return passengers


def run_simulation():
    elevator = Elevator(top_floor=24)
    passengers = generate_random_passengers(20)

    for iter in range(100):
        elevator.move()
        for passenger in passengers:
            passenger.move(elevator)
        print(elevator)
        sleep(1)


if __name__ == "__main__":
    run_simulation()
