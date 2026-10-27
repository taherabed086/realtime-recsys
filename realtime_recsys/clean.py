from pathlib import Path

from loguru import logger
import polars as pl
import typer

from realtime_recsys.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


def drop_zero_prices(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Remove rows whose price is zero or negative (a missing price, not a real one)."""
    return lf.filter(pl.col("price") > 0)


def clean_events(input_path: Path, output_path: Path) -> None:
    """Read the raw Parquet, apply the cleaning steps, and write the clean Parquet."""
    lf = pl.scan_parquet(input_path)
    lf = drop_zero_prices(lf)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lf.sink_parquet(output_path)


@app.command()
def main(
    input_path: Path = INTERIM_DATA_DIR / "events.parquet",
    output_path: Path = PROCESSED_DATA_DIR / "events_clean.parquet",
):
    logger.info(f"Cleaning {input_path} -> {output_path} ...")
    clean_events(input_path, output_path)
    logger.success("Cleaning complete.")


if __name__ == "__main__":
    app()
