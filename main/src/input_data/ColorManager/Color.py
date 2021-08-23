class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def to_hex(self):
        s = ""
        for c in (self.r, self.g, self.b):
            s += str(hex(c))[2:]
        return s