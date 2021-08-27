class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def to_hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"