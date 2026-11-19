# When to use dask

Dask is primarily a Python library, backed by a suite of tools, for building and running distributed, parallel, lazy computation pipelines.

## When to use Dask
- Your dataset is too big to fit into memory.
    - Often referred to as "out-of-core" computation.
- You have an expensive computational task that can be easily parallelised.
    - Often referred to as "embarrassingly parallel" computations.
    - An example would be depth averaging a field. This operation is embarrassingly parallel in time.

## When not to use Dask
As a rule-of-thumb: Whenever it can be avoided!
- If your data can be made to fit in memory.
    - If you only need a subset of your total data. Subset first and check if that fits in memory.
- "Shuffle-heavy" parallel tasks.
    - Tasks that require reorganising or sharing data between different partitions.

## Advantages of dask
- Strong compatibility with Python data science ecosystem
    - Familiar NumPy / Pandas style APIs
    - Built into Xarray and Pandas
        - Rarely have to interact with Dask itself
- Relatively simple to run on HPC Clusters
    - E.g. for running on _Sherlock_, there is a dedicated `SLURMCluster` interface for interacting with the SLURM scheduler
- Excellent dashboard for viewing the progress of big pipelines

## Disadvantages of dask
- Massive complexity overhead
    - Even a simple task requires setting up the full Dask pipeline: [task graph](02-the-task-graph.md), [scheduling](04-schedulers.md), etc.
- Easy to mess up
    - A bottleneck in any stage of the task graph will hold up the entire computation
    - Accidentally redo the same computations multiple times
- Debugging can be a nightmare