# basically this demonstrates that gevent & eventlet will mess up badly when you use non-thread safe code

###### Warning: while this is written for now EOLed stack, the results can be replicated for the recent most versions of python and/or celery as well


# Installation
1. have dependecies installed using `requirements.txt`
2. run redis on localhost: `docker run -d -p 6379:6379 redis`
3. init db: `python2 manage.py migrate`


# Trials
## Run with pool = `prefork`

*expectation* : No errors, everything runs fine. (ok there might be some database locked errors, but that's not what we're looking for)

1. run `python2 manage.py fill` to prefill the queue with tasks
2. run `celery worker -A demo -c 40 --pool prefork -l INFO` to run tasks


## Run with pool = `gevent`

*expectation* : few "IntegrityError: NOT NULL constraint failed: core_store.val", proving that shared state was mutated while the other thread was running concurrently.

1. run `python2 manage.py fill` to prefill the queue with tasks
2. run `celery worker -A demo -c 40 --pool gevent -l INFO` to run tasks


## Run with pool = `eventlet`

*expectation* : few "IntegrityError: NOT NULL constraint failed: core_store.val", proving that shared state was mutated while the other thread was running concurrently.

1. run `python2 manage.py fill` to prefill the queue with tasks
2. run `celery worker -A demo -c 40 --pool eventlet -l INFO` to run tasks


# conclusion

Stay the fuck away from `gevent` and `eventlet` if you have thread unsafe code, or you'll end up with inconsistent behaviour which can go catastrophically wrong.
