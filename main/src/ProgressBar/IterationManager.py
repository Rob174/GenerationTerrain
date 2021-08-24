class IterationManager:
    def __init__(self,total:int,step_size:int = 1):
        self.total = total
        self.step_size = step_size
        self.step = 0
    def next(self):
        self.step += self.step_size
        return self.step


        