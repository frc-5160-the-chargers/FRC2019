from components.hatch_extend import HatchExtend
from components.hatch_grab import HatchGrab

class HatchStates:
    RETRACTED = 0
    FULLYEXTENDED = 1
    GRABBEREXTENDED = 2
    RACKEXTENDED = 3

class HatchManager:
    hatch_extension : HatchExtend
    hatch_grabber : HatchGrab

    def __init__(self):
        self.currentState = HatchStates.RETRACTED

    def retract(self):
        self.hatch_extension.retract_hatch()
    
    def extend(self):
        self.hatch_extension.extend_hatch()

    def grab(self):
        self.hatch_grabber.grab_hatch()
    
    def release(self):
        self.hatch_grabber.release_hatch()

    def execute(self):
        if self.currentState == HatchStates.RETRACTED:
            self.retract()
            self.grab()
        if self.currentState == HatchStates.FULLYEXTENDED:
            self.extend()
            self.release()
        if self.currentState == HatchStates.GRABBEREXTENDED:
            self.retract()
            self.release()
        if self.currentState == HatchStates.RACKEXTENDED:
            self.extend()
            self.grab()

        self.hatch_extension.execute()
        self.hatch_grabber.execute()