from constants import UP_NAME, DOWN_NAME
from elevator import Elevator, Passenger
from exceptions import InvalidFloorError
from utils import set_elevator_for_passengers


class TestElevator:
    """Test suite for the Elevator class functionality."""

    def setup_method(self):
        """Setup for each test method; typically initializes the elevator object."""
        self.elevator = Elevator(top_floor=10)

    def teardown_method(self):
        """Teardown for each test method; typically cleans up the elevator object."""
        del self.elevator

    def test_elevator_door_operations(self):
        """Test the elevator's door opening and closing operations."""
        assert not self.elevator.doors_open

        self.elevator.open_doors()
        assert self.elevator.doors_open

        self.elevator.close_doors()
        assert not self.elevator.doors_open

    def test_of_permissible_floor_values(self):
        """The allowable default floor range is 1-10.
        @property does not allow to set values outside this range."""
        self.elevator.current_floor = 3
        try:
            self.elevator.current_floor = 12
        except InvalidFloorError:
            assert self.elevator.current_floor == 3

        try:
            self.elevator.current_floor = -4
        except InvalidFloorError:
            assert self.elevator.current_floor == 3

    def test_add_floor_to_queue(self):
        """Test the addition of floors to the elevator's queue."""
        self.elevator.add_floor_to_queue(3)
        assert self.elevator.queue == {3}

        self.elevator.add_floor_to_queue(2, 7, 9)
        assert self.elevator.queue == {2, 3, 7, 9}

    def test_remove_floor_from_queue(self):
        """Test the removal of floors from the elevator's queue."""
        self.elevator.add_floor_to_queue(2, 3, 7, 9)
        self.elevator.remove_floor_from_queue(3)
        assert self.elevator.queue == {2, 7, 9}

        self.elevator.remove_floor_from_queue(3)

    def test_choose_direction(self):
        """Test the elevator's direction choice based on its current state and queue."""
        self.elevator.add_floor_to_queue(3, 4, 8, 9)
        self.elevator.choose_direction()
        assert self.elevator.direction == UP_NAME

        self.elevator.direction = None
        self.elevator.current_floor = 6
        self.elevator.choose_direction()
        assert self.elevator.direction == DOWN_NAME

        self.elevator.direction = DOWN_NAME
        self.elevator.current_floor = 7
        self.elevator.choose_direction()
        assert self.elevator.direction == DOWN_NAME

        self.elevator.direction = UP_NAME
        self.elevator.current_floor = 5
        self.elevator.choose_direction()
        assert self.elevator.direction == UP_NAME

        self.elevator.direction = UP_NAME
        self.elevator.current_floor = 10
        self.elevator.choose_direction()
        assert self.elevator.direction == DOWN_NAME

        self.elevator.direction = UP_NAME
        self.elevator.queue = {2, 8}
        self.elevator.current_floor = 8
        self.elevator.choose_direction()
        assert self.elevator.direction == DOWN_NAME

        self.elevator.direction = UP_NAME
        self.elevator.current_floor = 8
        self.elevator.queue = {}
        self.elevator.choose_direction()
        assert not self.elevator.direction

    def test_move(self):
        """Test the elevator's movement between floors."""
        self.elevator.current_floor = 1
        self.elevator.add_floor_to_queue(3, 4, 6)
        self.elevator.move()
        self.elevator.move()
        assert self.elevator.current_floor == 3
        assert 3 not in self.elevator.queue

        self.elevator.add_floor_to_queue(1)
        self.elevator.move()
        assert self.elevator.current_floor == 4
        assert 4 not in self.elevator.queue

        self.elevator.move()
        self.elevator.move()
        assert self.elevator.current_floor == 6
        assert 6 not in self.elevator.queue

        self.elevator.move()
        assert self.elevator.current_floor == 5
        assert self.elevator.direction == DOWN_NAME

        for _ in range(5):
            self.elevator.move()
        assert self.elevator.current_floor == 1
        assert not self.elevator.direction

    def test_opening_closing_doors_when_moving_stopping(self):
        """Test the elevator's automatic door operations when moving and stopping."""
        self.elevator.add_floor_to_queue(2, 4)
        assert not self.elevator.doors_open

        self.elevator.move()
        assert self.elevator.current_floor == 2
        assert self.elevator.doors_open

        self.elevator.move()
        assert self.elevator.current_floor == 3
        assert not self.elevator.doors_open

    def test_overcapacity(self):
        """Test the elevator's behavior when its capacity is exceeded."""
        passengers = [
            Passenger(target_floor=3),
            Passenger(target_floor=4),
            Passenger(target_floor=5),
            Passenger(target_floor=6),
            Passenger(target_floor=7),
        ]
        set_elevator_for_passengers(passengers, self.elevator)
        self.elevator.current_floor = 1
        self.elevator.open_doors()
        self.elevator.capacity = 4
        for passenger in passengers:
            passenger.enter_the_elevator()
        assert len(self.elevator.passengers) == 5

        for passenger in passengers:
            passenger.select_floor()
        assert len(self.elevator.queue) == 5

        self.elevator.move()
        assert not self.elevator.doors_open
        assert len(self.elevator.passengers) == 4

    def test_abandon_ship(self):
        """Test the scenario where all passengers exit the elevator at their respective floors."""
        passengers = [
            Passenger(target_floor=3),
            Passenger(target_floor=4),
            Passenger(target_floor=5),
            Passenger(target_floor=6),
            Passenger(target_floor=7),
        ]
        set_elevator_for_passengers(passengers, self.elevator)
        self.elevator.current_floor = 1
        self.elevator.open_doors()
        self.elevator.capacity = 4
        for passenger in passengers:
            passenger.enter_the_elevator()
            passenger.select_floor()

        for floor in range(2, 8):
            self.elevator.move()
            if floor == 2:
                assert len(self.elevator.passengers) == 4
        assert not self.elevator.passengers

    def test_abandon_ship_together(self):
        """Test the scenario where multiple passengers exit the elevator at the same floor."""
        passengers = [
            Passenger(target_floor=3),
            Passenger(target_floor=4),
            Passenger(target_floor=4),
            Passenger(target_floor=6),
        ]
        set_elevator_for_passengers(passengers, self.elevator)
        self.elevator.current_floor = 1
        self.elevator.open_doors()
        for passenger in passengers:
            passenger.enter_the_elevator()
            passenger.select_floor()

        for floor in range(2, 7):
            self.elevator.move()
            if floor == 4:
                assert len(self.elevator.passengers) == 1
        assert not self.elevator.passengers

    def test_elevator_call_all_at_once(self):
        """Test the scenario where the elevator is called by all passengers at once."""
        passengers = [
            Passenger(current_floor=7, target_floor=3),
            Passenger(current_floor=1, target_floor=4),
            Passenger(current_floor=3, target_floor=4),
            Passenger(current_floor=9, target_floor=6),
        ]
        set_elevator_for_passengers(passengers, self.elevator)
        self.elevator.current_floor = 1
        for passenger in passengers:
            passenger.call_elevator()
        self.elevator.move()
        assert len(self.elevator.queue) == 3
        assert self.elevator.doors_open

        passengers[1].enter_the_elevator()
        passengers[1].select_floor()


class TestPassenger:
    """Test suite for the Passenger class functionality."""

    def setup_method(self):
        """Setup for each test method; typically initializes a passenger and elevator object."""
        self.passenger = Passenger(current_floor=1)
        self.elevator = Elevator(top_floor=20)
        set_elevator_for_passengers([self.passenger], self.elevator)

    def teardown_method(self):
        """Teardown for each test method; typically cleans up the passenger and elevator objects."""
        del self.passenger
        del self.elevator

    def test_name_generation(self):
        """Test the generation of a name for the passenger."""
        assert self.passenger.name

    def test_set_floor(self):
        """Test the passenger's ability to set a target floor."""
        self.passenger.target_floor = 2
        for _ in range(10):
            current_floor = self.passenger.current_floor
            self.passenger.set_a_new_target()
            assert self.passenger.target_floor != current_floor

    def test_call_elevator(self):
        """Test the passenger's ability to call the elevator."""
        self.passenger.target_floor = 4
        self.elevator.current_floor = 7
        self.passenger.call_elevator()
        assert self.elevator.queue == {1}

        for _ in range(6):
            self.elevator.move()

        assert self.elevator.current_floor == 1
        assert self.elevator.doors_open

    def test_passenger_enter_the_elevator(self):
        """Test the scenario where a passenger enters the elevator."""
        self.passenger.target_floor = 4
        self.elevator.current_floor = 7
        self.passenger.call_elevator()
        for _ in range(6):
            self.elevator.move()
        self.passenger.enter_the_elevator()
        assert self.passenger in self.elevator.passengers

    def test_passenger_select_floor(self):
        """Test the passenger's ability to select a floor inside the elevator."""
        self.passenger.target_floor = 4
        self.elevator.current_floor = 7
        self.passenger.call_elevator()
        for _ in range(6):
            self.elevator.move()
        self.passenger.enter_the_elevator()
        self.passenger.select_floor()
        assert self.passenger.target_floor in self.elevator.queue

    def test_passenger_cant_get_in_when_the_doors_are_closed(self):
        """Test the scenario where a passenger can't enter when the elevator's doors are closed."""
        self.passenger.target_floor = 4
        self.elevator.current_floor = self.passenger.current_floor
        self.passenger.enter_the_elevator()
        assert self.passenger not in self.elevator.passengers

    def test_passenger_leaving_the_elevator(self):
        """Test the scenario where a passenger exits the elevator upon reaching their target floor."""
        self.passenger.target_floor = 4
        self.elevator.current_floor = self.passenger.current_floor
        self.elevator.open_doors()
        self.passenger.enter_the_elevator()
        self.passenger.select_floor()
        for _ in range(3):
            self.elevator.move()
        assert self.passenger not in self.elevator.passengers
