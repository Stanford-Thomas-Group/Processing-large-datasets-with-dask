"""Visualise the task graph for computing the mean temperature before running it."""

from pathlib import Path

import xarray as xr

DATASET_PATH = Path(__file__).resolve().parent.parent / "datasets" / "example_temperature.nc"
FIGURE_DIR = Path(__file__).resolve().parent.parent / "figures" 

def main() -> None:
    FIGURE_DIR.mkdir(exist_ok=True)

    # open the dataset
    ds = xr.open_dataset(DATASET_PATH, chunks={})
    print(ds)
    ds["temperature"].data.visualize(filename=str(FIGURE_DIR / "temperature_dataset_task_graph.png"), rankdir="LR")

    # compute the mean temperature
    mean_temperature = ds["temperature"].mean(dim="time")   
    mean_temperature.data.visualize(filename=str(FIGURE_DIR / "temperature_mean_task_graph.png"), rankdir="LR")

    # compute the mean temperature and print the result
    print(mean_temperature.compute())


if __name__ == "__main__":
    main()
