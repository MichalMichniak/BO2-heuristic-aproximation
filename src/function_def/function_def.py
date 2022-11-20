
DISCONNECT_MSG = "DISCONECT"

def get_funct():
    return [(lambda x,y: x+y,12),
    (lambda x,y: x+y,13),
    (lambda x,y: x+y,4),
    (lambda x,y: x+y,5),
    (lambda x: x*2,10),
    (lambda x: x*2,5),
    (lambda x: x*2,8),
    (lambda x: x*2,2)]

def get_metric():
    return lambda x,y: (x-y)**2

def get_approx_funct():
    return lambda x,y: 0