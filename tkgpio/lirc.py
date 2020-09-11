from tkgpio import TkInfraredReceiver
from time import sleep

initialised = False
blocking = True

class LircConfig:
    def __init__(self):
        pass
        
    def add_config_file(self, config_filename):
        pass
    
    def code2char(self, code):
        pass
    
    def is_init_or_error(self):
        pass

def init(program_name, config_filename=None, blocking=True, verbose=False):
    lirc_socket = LircConfig()
    set_blocking(blocking, lirc_socket)
    
    global initialised
    if initialised:
        return
    
    receiver = TkInfraredReceiver()
    if receiver.config_name() == program_name:
        initialised = True
    
    return lirc_socket
    
def deinit():
    global initialised
    if not initialised:
        return

    initialised = False
    
def load_default_config():
    pass

def load_config_file(config_filename=None):
    pass

def nextcode():
    if not initialised:
        return []
    
    receiver = TkInfraredReceiver()
    code = receiver.get_next_code()
    if blocking == False:
        return code
    else:
        while code == []:
            code = receiver.get_next_code()
            sleep(0.1)
        
        return code
        
def set_blocking(_blocking, lirc_socket):
    global blocking
    blocking = _blocking