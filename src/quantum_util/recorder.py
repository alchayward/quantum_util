import asyncio
import functools
from decorator import decorator

import inspect

# Do I want to force kwargs to be recorded in args? 
# Does order of frozen set matter? 

@decorator
async def record_async(fn, cache: dict=None, fn_id: str =None, client=None, verbose: int=0, *args, **kw):
    fn_id = fn.__name__ if fn_id is None else fn_id
    
    if cache is None: cache = dict()
    if kw:  # frozenset is used to ensure hashability
        key = fn_id, args, frozenset(kw.items())
    else:
        key = fn_id, args

    # Learn KW order
    if key not in cache:
        if client is None:
            cache[key] = await fn(*args, **kw)
        else:
            cache[key] = await client.submit(fn, *(args +  tuple(kw.values())))
    return cache[key]

@decorator
def record(fn, cache: dict=None, fn_id: str =None, verbose: int=0, *args, **kw):
    fn_id = fn.__name__ if fn_id is None else fn_id
    
    
    if cache is None: cache = dict()
    
    if kw:  # frozenset is used to ensure hashability
        key = fn_id, args, frozenset(kw.items())
    else:
        key = fn_id, args

    if key not in cache:
        cache[key] = fn(*args, **kw)
    return cache[key]
 

# This has a weird interaction with record, because we don't want to distribute the cache,
# just the function itself. But means we should wrap with the distributed thing first, and then
# store the result once it's fniished. But  in this case we need to await the result in the memozie wrapper, and make this async. 
# Can we put a check for async in the momoize 

@decorator
async def dask_execute(fn, client=None, *args, **kwargs):
    result = await client.submit(fn, *args, key=(fn.__name__,args, kwargs) )
    return result
 
    



class Record:
    
    def __init__(self, dictionary=None, fn_name = None, verbose=0):
        
        
        self._dict = dictionary if dictionary is not None else dict()
        self.fn_name = fn_name

    def args_to_dict(self, args, kwargs):
        return str((self.fn_id,) + args + tuple(kwargs.items()))
        
    def get_args(self, fn):
        
        defaults = tuple() if fn.__defaults__ is None else fn.__defaults__
        n_kwargs =  len(defaults)
        n_args = fn.__code__.co_argcount - n_kwargs
        
        args = fn.__code__.co_varnames[:n_args]
        kwargs = fn.__code__.co_varnames[n_args:n_args+n_kwargs]
        defaults = fn.__defaults__
        return args, kwargs, defaults    

    
    def __call__(self, fn):
        self.fn = fn
        self.args, self.kwargs, self.defaults = self.get_args(fn)
        
        
            



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
    
    def get_args(self, fn):
        
        defaults = tuple() if fn.__defaults__ is None else fn.__defaults__
        n_kwargs =  len(defaults)
        n_args = fn.__code__.co_argcount - n_kwargs
        
        args = fn.__code__.co_varnames[:n_args]
        kwargs = fn.__code__.co_varnames[n_args:n_args+n_kwargs]
        defaults = fn.__defaults__
        return args, kwargs, defaults
    
    def decorate(self, fn):
        self.fn = fn
        self.args, self.kwargs, self.defaults = self.get_args(fn)
        
        @functools.wraps(fn)
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