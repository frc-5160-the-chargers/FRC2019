from components.hatch_extend import HatchExtend
from components.hatch_grab import HatchGrab

from utils import TimedState, TimedStateRunner, Timer, TimedStateRunnerChooser

class HatchStates:
    IDLE = 0
    RETRIEVAL = 1
    PLACING = 2
    RETRACTING = 3


class HatchManager:
    hatch_extension : HatchExtend
    hatch_grabber : HatchGrab

    def __init__(self):
        self.currentState = HatchStates.IDLE
        
        self.abortTimer = Timer()
        
        self.retrieval_released_aborted = TimedStateRunner([
            TimedState(0.2, self.retract),
            TimedState(0.0, self.grab)
        ])

        self.retrieval_released_normal = TimedStateRunner([
            TimedState(0.2, self.grab),
            TimedState(0.2, self.retract)
        ])

        self.retrieval_pressed_states = TimedStateRunner([
            TimedState(0.2, self.grab),
            TimedState(0.2, self.extend),
            TimedState(0.0, self.abortTimer.start()),
            TimedStateRunnerChooser(self.retrieval_released_aborted, self.retrieval_released_normal, self.aborted)
        ])

        self.placing_released_aborted = TimedStateRunner([
            TimedState(0.2, self.retract)
        ])

        self.placing_released_normal = TimedStateRunner([
            TimedState(0.2, self.release),
            TimedState(0.2, self.retract),
            TimedState(0.0, self.grab)
        ])

        self.placing_pressed_states = TimedStateRunner([
            TimedState(0.0, self.extend),
            TimedState(0.0, self.abortTimer.start()),
            TimedStateRunnerChooser(self.placing_released_aborted, self.placing_released_normal, self.aborted)
        ])

    def run_placing_routine(self):
        self.placing_pressed_states.execute()

    def run_retrieval_routine(self):
        self.retrieval_pressed_states.execute()

    def retrieval_pressed(self):
        self.retrieval_pressed_states.start()
        self.currentState = HatchStates.RETRIEVAL

    def aborted(self):
        return 1 if self.abortTimer.update() > 1.5 else 0

    def manuallyAbortAutomation(self):
        self.currentState = HatchStates.IDLE

    def placing_pressed(self):
        self.placing_pressed_states.start()
        self.currentState = HatchStates.PLACING

    def do_nothing(self):
        pass

    def retract_all(self):
        self.retract()
        self.grab()

    def retract(self):
        self.hatch_extension.retract_hatch()
    
    def extend(self):
        self.hatch_extension.extend_hatch()

    def grab(self):
        self.hatch_grabber.grab_hatch()
    
    def release(self):
        self.hatch_grabber.release_hatch()

    def execute(self):
        states = {
            HatchStates.IDLE : self.do_nothing,
            HatchStates.RETRIEVAL : self.run_retrieval_routine,
            HatchStates.PLACING : self.run_placing_routine,
            HatchStates.RETRACTING : self.retract_all
        }

        states[self.currentState]()

        self.hatch_extension.execute()
        self.hatch_grabber.execute()