from elevator import Elevator


class TestElevator:

    def setup_method(self):
        self.elevator = Elevator(top_floor=10)

    def teardown_method(self):
        del self.elevator

    def test_elevator_door_operations(self):
        assert not self.elevator.doors_open

        self.elevator.open_doors()
        assert self.elevator.doors_open

        self.elevator.close_doors()
        assert not self.elevator.doors_open

    def test_of_permissible_floor_values(self):
        """The allowable default floor range is 1-10.
        @property does not allow to set values outside this range."""
        self.elevator.current_floor = 3
        self.elevator.current_floor = 12
        assert self.elevator.current_floor == 3

        self.elevator.current_floor = -4
        assert self.elevator.current_floor == 3

    def test_add_floor_to_queue(self):
        self.elevator.add_floor_to_queue(3)
        assert self.elevator.queue == {3}

        self.elevator.add_floor_to_queue(2, 7, 9)
        assert self.elevator.queue == {2, 3, 7, 9}

    def test_remove_floor_from_queue(self):
        self.elevator.add_floor_to_queue(2, 3, 7, 9)
        self.elevator.remove_floor_from_queue(3)
        assert self.elevator.queue == {2, 7, 9}

        self.elevator.remove_floor_from_queue(3)

    def test_choose_direction(self):
        self.elevator.add_floor_to_queue(3, 4, 8, 9)
        self.elevator.choose_direction()
        assert self.elevator.direction == 'up'

        self.elevator.direction = None
        self.elevator.current_floor = 6
        self.elevator.choose_direction()
        assert self.elevator.direction == 'down'

        self.elevator.direction = 'down'
        self.elevator.current_floor = 7
        self.elevator.choose_direction()
        assert self.elevator.direction == 'down'

        self.elevator.direction = 'up'
        self.elevator.current_floor = 5
        self.elevator.choose_direction()
        assert self.elevator.direction == 'up'

        self.elevator.direction = 'up'
        self.elevator.current_floor = 10
        self.elevator.choose_direction()
        assert self.elevator.direction == 'down'

        self.elevator.direction = 'up'
        self.elevator.queue = {2, 8}
        self.elevator.current_floor = 8
        self.elevator.choose_direction()
        assert self.elevator.direction == 'down'

        self.elevator.direction = 'up'
        self.elevator.current_floor = 8
        self.elevator.queue = {}
        self.elevator.choose_direction()
        assert not self.elevator.direction

    def test_move(self):
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
        assert self.elevator.direction == 'down'

        for _ in range(5):
            self.elevator.move()
        assert self.elevator.current_floor == 1
        assert not self.elevator.direction

    def test_opening_closing_doors_when_moving_stopping(self):
        self.elevator.add_floor_to_queue(2, 4)
        assert not self.elevator.doors_open

        self.elevator.move()
        assert self.elevator.current_floor == 2
        assert self.elevator.doors_open

        self.elevator.move()
        assert self.elevator.current_floor == 3
        assert not self.elevator.doors_open
