# Define the states of the FSM
class States:
    START = 1
    RUNNING = 2
    PAUSED = 3
    STOPPED = 4

# Define the events that can trigger state transitions
class Events:
    START_BUTTON_PRESSED = 1
    STOP_BUTTON_PRESSED = 2
    PAUSE_BUTTON_PRESSED = 3
    RESUME_BUTTON_PRESSED = 4

# Define the FSM class
class FiniteStateMachine:
    def __init__(self):
        self.current_state = States.START

    def handle_event(self, event):
        # Define the state transition logic
        if self.current_state == States.START:
            if event == Events.START_BUTTON_PRESSED:
                self.current_state = States.RUNNING
                print("Started!")
            else:
                print("Invalid event in START state")
        elif self.current_state == States.RUNNING:
            if event == Events.STOP_BUTTON_PRESSED:
                self.current_state = States.STOPPED
                print("Stopped!")
            elif event == Events.PAUSE_BUTTON_PRESSED:
                self.current_state = States.PAUSED
                print("Paused!")
            else:
                print("Invalid event in RUNNING state")
        elif self.current_state == States.PAUSED:
            if event == Events.RESUME_BUTTON_PRESSED:
                self.current_state = States.RUNNING
                print("Resumed!")
            elif event == Events.STOP_BUTTON_PRESSED:
                self.current_state = States.STOPPED
                print("Stopped!")
            else:
                print("Invalid event in PAUSED state")
        elif self.current_state == States.STOPPED:
            if event == Events.START_BUTTON_PRESSED:
                self.current_state = States.RUNNING
                print("Started!")
            else:
                print("Invalid event in STOPPED state")

    def get_current_state(self):
        return self.current_state

# Create an instance of the FSM
fsm = FiniteStateMachine()

# Simulate some events
fsm.handle_event(Events.START_BUTTON_PRESSED)  # Started!
fsm.handle_event(Events.PAUSE_BUTTON_PRESSED)  # Paused!
fsm.handle_event(Events.RESUME_BUTTON_PRESSED)  # Resumed!
fsm.handle_event(Events.STOP_BUTTON_PRESSED)  # Stopped!
fsm.handle_event(Events.START_BUTTON_PRESSED)  # Started!