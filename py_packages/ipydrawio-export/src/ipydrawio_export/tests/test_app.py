def test_app_args(export_app):
    assert not export_app.dio_files
    export_app.parse_command_line(["foo.dio"])
    assert export_app.dio_files
