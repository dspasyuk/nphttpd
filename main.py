from uhttpd import httserv
try:
   httserv()
except OSError:
    import machine
    machine.reset()
    pass
    
