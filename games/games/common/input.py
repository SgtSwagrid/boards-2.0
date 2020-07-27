class ClickInput:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Controller:

    def __init__(self, selected=None):
        self.selected = selected if selected else set()

    def select(self, x, y):
        return Controller(selected=self.selected | {(x, y)})

    def unselect(self, x, y):
        return Controller(selected=self.selected - {(x, y)})

    def clear(self):
        return Controller(selected=set())

    def num_selected(self):
        return len(self.selected)

    def is_selected(self, x, y):
        return any(s == (x, y) for s in self.selected)

    def first_selected(self):
        return next(iter(self.selected))