from nphttpd import HttServ
try:
    HttServ()
except OSError:
    import machine
    machine.reset()
    pass
    
