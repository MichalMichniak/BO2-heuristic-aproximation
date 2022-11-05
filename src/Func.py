class Func:
    """
    abstract function class
    """
    def __init__(self,time : float = 0, n_param = 1) -> None:
        """
        args:
            time : float - propagation time
            n_param : int - parameter count
        """
        self.time : float = time
        self.n_param = n_param
        pass

    def get_time(self)-> float:
        """
        return:
            time : float - propagation time
        """
        return self.time

    def set_time(self,new_time : float) -> None:
        """
        args:
            new_time : float - new propagation time
        """
        self.time = new_time