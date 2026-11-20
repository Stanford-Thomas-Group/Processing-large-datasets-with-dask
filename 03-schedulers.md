# Schedulers

It is the job of the scheduler to execute the task graph. There are two families of scheduler. First, the single machine schedulers and then second, the distributed scheduler. Although, slightly confusingly the distributed scheduler can still be used on a single machine.

## Local thread pool
This is the default scheduler for dask arrays. It runs in a single process on a single machine, but will use all available threads. To force this as the scheduler
```python
import dask
dask.config.set(scheduler='threads')  # overwrite default with threaded scheduler
```

### Advantages
- Simple.
- Very little overhead to executing tasks.
- No cost to transfer data between tasks.

### Disadvantages
- Limited parallelism.
    - Python's Global Interpreter Lock (GIL) means that all python code is single threaded. 
    - Non-python code, e.g. numpy internals, can utilise multiple threads.

## Single thread
The single threaded, or `synchronous`, scheduler has no parallelism. This is handy for debugging, but less useful for running full pipelines. To set this scheduler:
```python
import dask
dask.config.set(scheduler='synchronous')  # overwrite default with single-threaded scheduler
```

## Local processes
There's also the option to use local processes to parallelise the code. However, this is no longer recommended. It has been superseded by running the distributed scheduler (below) over a local cluster.

## Distributed
The distributed scheduler requires a cluster of workers and a client to interact with the cluster. The distributed scheduler then hands off tasks to the workers. A nice feature of the distributed schedule is that the client provides a dashboard for keeping track of your computation.

### Local cluster
The simplest cluster is the ``LocalCluster`` which runs on a single machine. It can be created explicitly with
```python
from dask.distributed import Client, LocalCluster

if __name__ == "__main__":
    cluster = LocalCluster(n_workers=4, threads_per_worker=2, memory_limit="4GB")
    client = Client(cluster)
```
This setup is very useful when running in an interactive job on an HPC Cluster. For example suppose we ask for the following allocation:
```bash
salloc -p serc -t 2:00:00 --nodes 1 --ntasks 4 --cpus-per-task 2 --mem-per-cpu 8G
```
Then in our python script or notebook we can use
```python
import os
from dask.distributed import Client, LocalCluster

NTASKS = int(os.environ["SLURM_NTASKS"])
CPUS_PER_TASK = int(os.environ["SLURM_CPUS_PER_TASK"])
MEM_PER_CPU = int(os.environ["SLURM_MEM_PER_CPU"])  # in MiB

if __name__ == "__main__":
    cluster = LocalCluster(
        n_workers=NTASKS, 
        threads_per_worker=CPUS_PER_TASK, 
        memory_limit=f"{MEM_PER_CPU * CPUS_PER_TASK}MiB"
    )
    client = Client(cluster)
```

The ``LocalCluster`` is the default so it is possible to simply write

```python
from dask.distributed import Client

if __name__ == "__main__":
    client = Client()
```

> [!WARNING]
> When running a ``LocalCluster`` in a script it is essential to place it within an ``if __name__ == "__main__":`` block. When launching the worker subprocesses, Dask spawns a new python interpreter that re-imports the main script. Without the guard, the new process would attempt to spawn it's own set of workers. You would have effectively created a fork bomb. 

> [!NOTE]
> Jupyter notebooks use a different system so creating a ``LocalCluster`` is totally safe.

### SLURMCluster

An alternative way to set up a cluster on a SLURM managed system is to use a ``SLURMCluster``. Rather than asking for all your computational resources upfront. It is possible to set up a cluster by requesting new resources for each worker. The ``SLURMCluster`` handles the submitting of request to the SLURM scheduler and then tasks can be allocated to workers as they come online. 

This way of working is very useful if you've already started an interactive job and discover you need more resources. Or you have a workflow combining parallelisable and serial components. It's also nice that a small upfront allocation will become available quickly. If you're developing a new notebook, you might ask for a small interactive allocation, then submit the request for your computational resources through the ``SLURMCluster``. You can then write the rest of your notebook while those additional resources slowly come online.