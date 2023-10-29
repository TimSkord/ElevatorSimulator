from interfaces import ElevatorInterface
from utils import find_closest, has_larger, has_smaller
from random import choice


class Elevator(ElevatorInterface):

    def __init__(self, capacity=4, lower_floor=1, top_floor=10):
        self.lower_floor = lower_floor
        self.top_floor = top_floor
        self.capacity = capacity

        self.doors_open = False
        self._current_floor = self.lower_floor
        self.direction = None
        self.queue = set()
        self.passengers = set()
        self.directions = {
            None: self.set_idle,
            "up": self.up_one_floor,
            "down": self.down_one_floor,

        }

    @property
    def state(self):
        if self.direction:
            return f"move_{self.direction}"
        return 'idle'

    @property
    def current_floor(self):
        return self._current_floor

    @current_floor.setter
    def current_floor(self, new_floor):
        if self.lower_floor <= new_floor <= self.top_floor:
            self._current_floor = new_floor

    @property
    def movement_permitted(self):
        return len(self.passengers) <= self.capacity

    def to_push_a_random_person_out_of_an_elevator(self):
        if self.movement_permitted:
            return
        weakest_link = choice(list(self.passengers))
        self.passengers.remove(weakest_link)
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

    def check_queue(self):
        if self.queue:
            self.choose_direction()

    def passengers_getting_off(self, passenger_list: set):
        map(lambda passenger: passenger.set_floor(self.current_floor), passenger_list)
        self.passengers -= passenger_list

    def passengers_entering(self, passenger):
        self.passengers.add(passenger)
        print(f"{passenger} stepped into the elevator as if it were his home.")

    def check_passengers(self):
        who_go_out = set()
        for passenger in self.passengers:
            if passenger.target_floor == self.current_floor:
                who_go_out.add(passenger)
        if self.current_floor in self.queue:
            self.open_doors()
            self.passengers_getting_off(who_go_out)
            self.remove_floor_from_queue(self.current_floor)

    def check_doors(self):
        if self.doors_open:
            self.close_doors()

    def choose_direction(self) -> None:
        sorted_queue = sorted(self.queue)
        closest_floor = find_closest(sorted_queue, self.current_floor)
        calls_above = has_larger(sorted_queue, self.current_floor)
        calls_below = has_smaller(sorted_queue, self.current_floor)

        if not closest_floor:
            self.direction = None
        elif not self.direction:
            if closest_floor > self.current_floor:
                self.direction = 'up'
            elif closest_floor < self.current_floor:
                self.direction = 'down'
        elif self.direction == 'up' and (not calls_above and calls_below):
            self.direction = 'down'
        elif self.direction == 'down' and (not calls_below and calls_above):
            self.direction = 'up'

    def move(self) -> None:
        if self.queue:
            self.to_push_a_random_person_out_of_an_elevator()
            self.choose_direction()
            move_toward = self.directions[self.direction]
            self.check_doors()
            move_toward()
        else:
            self.set_idle()

    def set_idle(self):
        self.direction = None

    def up_one_floor(self):
        self.current_floor += 1
        print(f"The elevator arrived on the {self.current_floor} floor.")
        self.check_passengers()

    def down_one_floor(self):
        self.current_floor -= 1
        print(f"The elevator arrived on the {self.current_floor} floor.")
        self.check_passengers()

    def __str__(self):
        message = f"""
        Floor: {self.current_floor}
        Passengers: {self.passengers}
        Directions: {self.direction}
        Queue: {self.queue}
        """
        return message
