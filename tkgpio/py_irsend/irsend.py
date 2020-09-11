from tkgpio import TkInfraredEmitter


def list_remotes(device=None, address=None):
    emitter = TkInfraredEmitter()
    return emitter.list_remotes()


def list_codes(remote, device=None, address=None):
    emitter = TkInfraredEmitter()
    return emitter.list_codes(remote)


def send_once(remote, codes, count=None, device=None, address=None):
    # simulate original error if codes is not a list
    codes = [] + codes
    
    emitter = TkInfraredEmitter()
    emitter.send_once(remote, codes, count)


def send_start(remote, code, device=None, address=None):
    pass


def send_stop(remote, code, device=None, address=None):
    pass


def set_transmitters(transmitters, device=None, address=None):
    pass