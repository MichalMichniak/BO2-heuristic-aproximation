class Func:
    def __init__(self,time : float = 0):
        self.time : float = time
        pass

    def get_time(self)-> float:
        return self.time

    def set_time(self,new_time : float):
        self.time = new_time