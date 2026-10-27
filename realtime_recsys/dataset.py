from pathlib import Path

from loguru import logger
import polars as pl
import typer

from realtime_recsys.config import INTERIM_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

# Column types of the raw CSV. event_time is read as text first, then parsed.
CSV_SCHEMA = {
    "event_time": pl.String,
    "event_type": pl.String,
    "product_id": pl.Int64,
    "category_id": pl.Int64,
    "category_code": pl.String,
    "brand": pl.String,
    "price": pl.Float64,
    "user_id": pl.Int64,
    "user_session": pl.String,
}


def csv_to_parquet(input_path: Path, output_path: Path) -> None:
    """Convert the raw events CSV to Parquet without loading it fully in memory.

    This is a raw conversion: no rows are removed or changed, only column types are fixed.
    """
    lazy = pl.scan_csv(input_path, schema=CSV_SCHEMA).with_columns(
        pl.col("event_time").str.to_datetime("%Y-%m-%d %H:%M:%S UTC", time_zone="UTC"),
        pl.col("event_type").cast(pl.Categorical),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lazy.sink_parquet(output_path)


@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "2019-Oct.csv",
    output_path: Path = INTERIM_DATA_DIR / "events.parquet",
):
    logger.info(f"Converting {input_path} to {output_path} ...")
    csv_to_parquet(input_path, output_path)
    logger.success("Conversion complete.")


if __name__ == "__main__":
    app()
