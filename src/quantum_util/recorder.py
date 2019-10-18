

class Recorder():
    
    def __init__(self, db, fn_id, verbose=0):
        self._dict = db
        self.num_loaded = 0
        self.num_run = 0
        self.fn_id = fn_id
        self.verbose = verbose
    
    def v_print(self, msg, vl):
        if self.verbose >= vl: print(msg)
    
    def args_to_dict(self, args, kwargs):
        return str((self.fn_id,) + args + tuple(kwargs.items()))
        
    def decorate(self, fn):
        def new_fn(*args, **kwargs):
            d = self.args_to_dict(args, kwargs)
            try:
                out = self._dict[d]
                self.num_loaded += 1
            except KeyError:
                out = fn(*args, **kwargs)
                self._dict[d] = out
                self.num_run += 1

            return out
        return new_fn


