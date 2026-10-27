import polars as pl

from realtime_recsys.clean import drop_zero_prices


def test_drop_zero_prices_keeps_only_positive_prices():
    lf = pl.LazyFrame({"product_id": [1, 2, 3, 4], "price": [10.5, 0.0, -1.0, 0.01]})

    result = drop_zero_prices(lf).collect()

    assert result["product_id"].to_list() == [1, 4]
