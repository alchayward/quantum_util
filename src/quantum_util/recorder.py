import asyncio

class Recorder():
    
    def __init__(self, db, fn_id, verbose=0, save_fn=None):
        self._dict = db
        self.num_loaded = 0
        self.num_run = 0
        self.fn_id = fn_id
        self.verbose = verbose
        self._save_fn = save_fn
    
    def dump(self):
        try:
            self._save_fn()
        except TypeError:
            print('save function not defined')

    def v_print(self, msg, vl):
        if self.verbose >= vl: print(msg)
    
    def args_to_dict(self, args, kwargs):
        return str((self.fn_id,) + args + tuple(kwargs.items()))
    
    def get_args(fn):
        
        defaults = fn.__defaults__
        n_kwargs = len(defaults)
        n_args = fn.__code__.co_argcount - n_kwargs
        
        args = fn.__code__.co_varnames[:n_args]
        kwargs = fn.__code__.co_varnames[n_args:n_args+n_kwargs]
        defaults = fn.__defaults__
        return args, kwargs, defaults
    
    def decorate(self, fn):
        self.fn = fn
        self.args, self.kwargs, self.defaults = self.get_args(fn)
        
        
        def new_fn(*args, **kwargs):
            d = self.args_to_dict(args, kwargs)
            try:
                out = self._dict[d]
                self.num_loaded += 1
            except KeyError:
                out = self.fn(*args, **kwargs)
                self._dict[d] = out
                self.num_run += 1

            return out
        return new_fn

class ParallelRecorder(Recorder):
    # Want a recorder that can run these functions easily in parallel.

    def __init__(self, db, fn_id, client,  verbose=0, fn=None, save_fn=None):
        self._dict = db
        self.num_loaded = 0
        self.num_run = 0
        self.fn_id = fn_id
        self.verbose = verbose
        self.client = client
        self.fn = fn
        self.futures = []
        self._save_fn = save_fn

    def decorate(self, fn):
        self.fn = fn

        async def new_fn(*args, **kwargs):
            d = self.args_to_dict(args, kwargs)
            try:
                out = self._dict[d]
                self.num_loaded += 1
            except KeyError:
                out = await self.client.submit(self.fn, *args, key=d)
                self._dict[d] = out
                self.num_run += 1

            return out
        return new_fn

class RecorderDF():
    
    def __init__(self, db, fn_id, verbose=0, save_fn=None):
        self._dict = db
        self.num_loaded = 0
        self.num_run = 0
        self.fn_id = fn_id
        self.verbose = verbose
        self._save_fn = save_fn
    
    def dump(self):
        try:
            self._save_fn()
        except TypeError:
            print('save function not defined')

    def v_print(self, msg, vl):
        if self.verbose >= vl: print(msg)
    
    def get_args(fn):
        
        defaults = fn.__defaults__
        n_kwargs = len(defaults)
        n_args = fn.__code__.co_argcount - n_kwargs
        
        args = fn.__code__.co_varnames[:n_args]
        kwargs = fn.__code__.co_varnames[n_args:n_args+n_kwargs]
        defaults = fn.__defaults__
        return args, kwargs, defaults
    
    def decorate(self, fn):
        self.fn = fn
        self.args, self.kwargs, self.defaults = self.get_args(fn)
        
        
        def new_fn(*args, **kwargs):
            d = self.args_to_dict(args, kwargs)
            try:
                out = self._dict[d]
                self.num_loaded += 1
            except KeyError:
                out = self.fn(*args, **kwargs)
                self._dict[d] = out
                self.num_run += 1

            return out
        return new_fn