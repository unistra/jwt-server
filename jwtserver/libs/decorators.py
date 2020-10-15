import json
import time


class MemoizeWithTimeout(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=300):
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        ct = time.time()
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (ct - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self._caches.setdefault(f, {})
        cache = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            ar = tuple([item if isinstance(item, str) else json.dumps(item) for item in args])
            kw = sorted(kwargs.items())
            key = (ar, tuple(kw))
            try:
                v = self._caches[f][key]
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                result = f(*args, **kwargs), time.time()
                v = cache[key] = result
                self._caches[f] = cache
            return v[0]

        func.func_name = f.__name__
        return func
