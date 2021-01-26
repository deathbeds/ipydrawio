def test_provision(provision_app, tmp_path):
    provision_app.start()
    assert [*tmp_path.glob("*")]
