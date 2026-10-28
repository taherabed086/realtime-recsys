import polars as pl

from realtime_recsys.clean import drop_duplicate_rows, drop_zero_prices


def test_drop_zero_prices_keeps_only_positive_prices():
    df = pl.DataFrame({"product_id": [1, 2, 3, 4], "price": [10.5, 0.0, -1.0, 0.01]})

    result = drop_zero_prices(df)

    assert result["product_id"].to_list() == [1, 4]


def test_drop_duplicate_rows_keeps_one_copy():
    df = pl.DataFrame(
        {
            "user_id": [1, 1, 1, 2],
            "event_type": ["cart", "cart", "view", "cart"],
            "price": [5.0, 5.0, 5.0, 5.0],
        }
    )

    result = drop_duplicate_rows(df)

    assert result.height == 3


def test_drop_duplicate_rows_keeps_original_order():
    df = pl.DataFrame({"t": [3, 1, 3, 2, 1]})

    result = drop_duplicate_rows(df)

    assert result["t"].to_list() == [3, 1, 2]
