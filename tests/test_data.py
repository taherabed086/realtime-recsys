def test_package_imports():
    """Smoke test: the package can be imported (setup is working)."""
    import realtime_recsys

    assert realtime_recsys is not None
