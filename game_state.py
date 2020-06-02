
class State:
    def __init__(self):
        self.done = False
        self.started = False
        self.run = False
        self.running = False
        self.has_computed = False
        self.mouse_down = False
        self.dragging = False
        self.special_to_move = None
        self.recalculate = False
        self.cut_pathing = False
        self.pos = None
        self.button = None
        self.drawing = False

    def cleanup(self):
        self.dragging = False
        self.special_to_move = None
        self.drawing = False
        self.button = None
        self.pos = None

