"""Create the example temperature dataset tracked in this repo."""

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "datasets" / "example_temperature.nc"

N_TIME = 20
N_LAT = 20


def build_dataset() -> xr.Dataset:
    time = pd.date_range("2026-01-01", periods=N_TIME, freq="D")
    latitude = np.linspace(-45, 45, N_LAT)

    temperature = 15 - 0.2 * latitude[np.newaxis, :] + 2 * np.sin(
        2 * np.pi * np.arange(N_TIME)[:, np.newaxis] / N_TIME
    )

    ds = xr.Dataset(
        {"temperature": (("time", "latitude"), temperature)},
        coords={"time": time, "latitude": latitude},
    )
    ds["temperature"].attrs["units"] = "degC"
    ds["latitude"].attrs["units"] = "degrees_north"

    return ds


def main() -> None:
    ds = build_dataset()
    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    encoding = {"temperature": {"chunksizes": (N_TIME // 2, N_LAT)}}
    ds.to_netcdf(OUTPUT_PATH, encoding=encoding)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
