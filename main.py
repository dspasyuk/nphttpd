from neo import ledserv
try:
   httserv()
except OSError:
    import machine
    machine.reset()
    pass
    
