# **Elevator Simulation Project**
This project simulates the operations of an elevator system. It includes both elevator and passenger behaviors, providing a detailed understanding of how passengers interact with the elevator and how the elevator responds to different scenarios.

![img.png](static/elevator_crash.png)

## **Elevator Illustration**

### **Features**
* **Elevator Movements**: The elevator can move up, down or stay idle depending on passenger requests and its current queue.
* **Dynamic Passenger Behavior**: Passengers can call the elevator, enter it, select their target floor, and exit once they reach their destination.
* **Capacity Control**: The elevator has a defined capacity, and if it's exceeded, random passengers are ejected.
* **Intelligent Direction Logic**: The elevator chooses its direction based on the current queue of floor requests and the locations of passengers inside.

## **Classes**

### `Elevator`
Represents the elevator system. It includes methods for moving the elevator, managing the passengers inside, and controlling the doors.

### `Passenger`
Simulates the behavior of a passenger. A passenger can call the elevator, set a target floor, and get in or out of the elevator.

## **Usage**
1. Create instances of the elevator and passenger classes.
2. Define elevator to the user.
3. Simulate elevator movements and interactions using the provided methods.

```python
elevator = Elevator()
passenger = Passenger(name="John", current_floor=1, target_floor=5)
passenger.set_elevator(elevator)

passenger.call_elevator()
elevator.move()
# ... continue simulation
```

## **Installation**

1. Clone the repository:
    ```shell
    git clone https://github.com/TimSkord/ElevatorSimulator.git
    ```

2. Navigate to the project directory:
   ```shell
   cd ElevatorSimulator
   ```
3. Install the required packages:
   ```shell
   pip install -r requirements.txt  
   ```
4. Run the simulation script:
   ```shell
   python main.py   
   ```
   
## **Tests**

1. Run the following command to run the tests:
   ```shell
   pytest
   ```

## **Contribution**
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.