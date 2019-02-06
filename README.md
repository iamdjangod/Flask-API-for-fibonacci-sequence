
_Adnymics Developer Task._

**Table of Contents**

  - [About](#about)
  - [Requirements](#requirements)
  - [Run](#run)
  - [Request](#request)
  - [Response](#response)
  - [Performance](#performance)
  - [Notes](#notes)
  - [Development Guide](#development-guide)
  - [Future Work](#future-work)

# About

**Fibonacci Server** is a RESTful web service that provides the [Fibonacci
number](https://en.wikipedia.org/wiki/Fibonacci_number) (starts from 0) for any
given integer less than a predefined number (10,000 for now, see
["Performance"](#performance) section below).


# Requirements

Fibonacci Server requires

- Python 2.6+, 3.3+ or pypy (verified on 2.6, 2.7, 3.3, 3.4, 3.5 and pypy)
- [Flask](http://flask.pocoo.org/) web framework, which you can install with
  [pip](https://pip.pypa.io/en/stable/)

In general, you just need to bootstrap pip if you don't have that available on
your system and use it to install Flask.  Here's how:

```
$ which pip || curl -fsSL https://bootstrap.pypa.io/get-pip.py | sudo python
$ sudo pip install flask
```

If you prefer to install as non-root user, consider use
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

# Run

Just clone the source code, enter the directory and run:

```
$ ./fibonacci_server.py &
```

This will run the service and listen on port `8080` (use option `-p|--port N`
to change the default port). Now the service is running and ready to serve,
logs go to `runtime.log`.

Full usage can be shown with option `--help`:

```
$ ./fibonacci_server.py --help
Usage: fibonacci_server.py [options]

Options:
  -h, --help            show this help message and exit
  -b BIND, --bind=BIND  Bind address, default 127.0.0.1, use "0.0.0.0" for all
  -p PORT, --port=PORT  Listen port, default is 8080
```

# Request

The request format is `GET /fib/first_idx/end_idx`, where

- `first_idx` is a non-negative integer represents the **first `number` numbers**
  and `first_idx` is a non-negative integer represents the **second `number` numbers** of the Fibonacci sequence

For example:

```
$ curl -is localhost:8080/fib/1/5
```

This should give you an JSON blob (array) `[1, 1, 2, 3, 5]` in the body as well
as a normal status code `200` in the header.  See more status codes below.

# Response

Response is a status code with human readable message in HTTP header and a JSON
array in body text.  Note body text might contain unexpected HTML entities so
a client should always check HTTP status code before parsing the body as JSON.

Status codes are listed below.

| Status Code   | Message                  | Explanation                                       |
| ------------- | ------------------------ | ------------------------------------------------- |
| 200           | OK                       | Success, result JSON will be in body              |
| 400           | BAD REQUEST              | Input is invalid (not an integer or is negative)  |
| 413           | REQUEST ENTITY TOO LARGE | Given number too large                            |
| 500           | INTERNAL SERVER ERROR    | Unknown error happened on server side (check log) |
| 501           | NOT IMPLEMENTED          | Not supported API version                         |

See also [List of HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

# Performance

**The Fibonacci Algorithm**

- Counting 10,000 numbers takes _7 ms_
- Counting 100,000 numbers takes _330 ms_
- Counting 500,000 numbers takes _61 s_

These were done on a pretty recent MBP with 8G memory and python 2.7.10.  Note
this is only for the first call for uncached numbers, the implementation has
a singleton instance and caches all the results as it is runs.  Another good
thing is it does not use recursion so _no max recursion depth limit_ at all.

```
$ python fibonacci.py 10000
         10003 function calls in 0.007 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.007    0.007 <string>:1(<module>)
        1    0.007    0.007    0.007    0.007 fibonacci.py:42(__compute)
        1    0.000    0.000    0.007    0.007 fibonacci.py:56(sequence)
        1    0.000    0.000    0.000    0.000 {len}
     9998    0.001    0.000    0.001    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

$ python fibonacci.py 100000
         100003 function calls in 0.330 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.330    0.330 <string>:1(<module>)
        1    0.321    0.321    0.328    0.328 fibonacci.py:42(__compute)
        1    0.003    0.003    0.330    0.330 fibonacci.py:56(sequence)
        1    0.000    0.000    0.000    0.000 {len}
    99998    0.006    0.000    0.006    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

$ python fibonacci.py 500000
         500003 function calls in 61.763 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003   61.763   61.763 <string>:1(<module>)
        1   21.992   21.992   22.061   22.061 fibonacci.py:46(__compute)
        1   39.699   39.699   61.760   61.760 fibonacci.py:60(sequence)
        1    0.000    0.000    0.000    0.000 {len}
   499998    0.069    0.000    0.069    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

On the other hand, size of response body reaches _10MB_ for _n=10,000_ and
_~1GB_ for _n=100,000_, so limit the `fibonacci_server` to accept a number **<=
10000** would be reasonable in both response time and size.

```
$ python fibonacci.py 100 | wc -c     # 1259
$ python fibonacci.py 1000 | wc -c    # 107450 (105K)
$ python fibonacci.py 10000 | wc -c   # 10479753 (10M)
$ python fibonacci.py 50000 | wc -c   # 261386761 (249M)
$ python fibonacci.py 100000 | wc -c  # 1045242714 (996M)
```

**The Fibonacci Server**

Since the underlying Fibonacci computing instance is a singleton instance and
it caches all the results it has computed, performance of the Fibonacci Server
is not a thing to worry at all, it just a wrapper on top of the computing
instance using the Flask web framework.  What does need to worry about are:

- Performance of the Flask framework itself
- Performance of json.dumps(), for our simple use case we can write
  a C extension when it becomes a bottleneck

# Notes

Focused on core features first

- [X] The algorithm
- [X] The web service
- [X] Command line option
- [X] Performance
- [X] Logging with rotation support

Followed engineering best practices

- [X] Implemented code lint check (pep8)
- [X] Implemented unit tests and coverage report
- [X] Implemented functional tests
- [X] Iterated the work, each with a short living git branch

# Development Guide

Highly recommend to use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
so that to develop with different isolated python versions.  Once you have
virtualenv bootstrapped (refer to ["Requirements"](#requirements) section),
download different python versions (2.6, 2.7 and latest 3.x) from
[python.org](http://python.org/) and install to your system, and then -

Initialize virtual envs:

```
$ virtualenv -p `which python2.6` envs/2.6
$ virtualenv -p `which python2.7` envs/2.7
$ virtualenv -p `which python3.5` envs/3.5
```

To work with specific python version, for example 2.6:

```
$ source envs/2.6/bin/activate
$ pip install -r requirements.txt
$ make
```

To exit a virtual env:

```
$ deactivate
```

# Future Work

following work needs to be considered as
well:

- Start/stop scripts
- Auto deployment (shippable package, auto versioning based on git tag)
- Auto start across reboot
- Monitoring mechanism (pid check, url check, performance check)

If performance is a big deal, we should

- Evaluate existing python web frameworks to select the best one
- Rewrite the `json.dumps()` with C extension
- Run multiple threads or instances on a single node and share the singleton
  _Fibonacci_ object (shared memory)
- Consider use other language, for example golang, to get better performance

We can also consider implement a **distributed version**

- Pre-compute Fibonacci sequence and store in centralized manner (Redis?
  Memcached?)
- Add a load balancer in front of multiple service nodes (HAProxy?)
