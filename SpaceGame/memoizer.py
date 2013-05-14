def memoizer(new_dict=dict):
    """
    Creates a memoizer with the given dictionary policy.
 
    The memoizer thus obtained can be used as a decorator to remember the
    results of calls to long-running functions, such as loading images
    from disk. It also means that there will only be one copy of the image,
    which can be quite handy when dealing with restricted resources.
 
    Example:
 
    weak_memoize = memoize(new_dict=weakref.WeakValueDictionary)
 
    @weak_memoize
    def load_image(filename):
        # Your long running image-loading code goes here.
        return result
        
    """
    def memoize(func):
        cache = new_dict()
 
        def memo(*args, **kwargs):
            try:
                # Create a key, resorting to repr if the key isn't hashable.
                try:
                    k = (args, tuple(kwargs.items()))
                    hash(k)
                except TypeError:
                    k = repr(k)
                    
                # Try to return the result from the cache.
                return cache[k]
            except KeyError:
                # The key wasn't found, so invoke the function and save the
                # result in the cache.
                result = func(*args, **kwargs)
                cache[k] = result
                return result
            
        return memo
    
    return memoize
