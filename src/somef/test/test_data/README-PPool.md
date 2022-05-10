# PPool
PPool is a Pool for Processes in Python with locks. The main advantage is the ability to use `Lock`s from  `multiprocessing`

[![PyPI version](https://badge.fury.io/py/PPool.svg)](https://badge.fury.io/py/PPool)

# Install
```
pip install PPool
```

# pypi
`https://pypi.org/project/PPool/`


# Example
```
from PPool.Pool import Pool
params = [('A', 2),('B', 3),('C', 4), ('D', 5)]

def foo(name, num):
    print(name+str(num))

pool = Pool(max_num_of_processes=3, func=foo, params_list=params)

pool.run()
```