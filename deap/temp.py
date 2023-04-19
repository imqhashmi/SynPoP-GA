from joblib import Parallel, delayed, parallel_backend
def loop_function(x):
    return x**2

inputs = [1, 2, 3, 4, 5]
num_jobs = 16
results = Parallel(n_jobs=num_jobs)(delayed(loop_function)(x) for x in inputs)
print(results)
