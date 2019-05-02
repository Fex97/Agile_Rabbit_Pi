def foo(bar,baz):
	while True:
		print('hello {0}'.format(bar))
		return 'foo'+baz


from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)

async_result = pool.apply_async(foo,('world','foo'))

return_val = async_result.get()
print(return_val)
