import importlib.util
import json
import os

_SCRIPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "scripts",
    "gen_currency_data.py",
)


def _load_module():
    spec = importlib.util.spec_from_file_location("gen_currency_data", _SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_load_source_dict_reads_a_currency_db_from_a_python_file(tmp_path):
    module = _load_module()
    source = tmp_path / "source.py"
    source.write_text(
        'CURRENCY_DB = {"USD": {"name": "US Dollar", "code": "USD", '
        '"symbol": "$", "country": "US", "flag": "🇺🇸", "type": "Fiat"}}'
    )

    result = module.load_source_dict(str(source))

    assert result["USD"]["name"] == "US Dollar"


def test_round_trips_a_currency_db_to_json_files(tmp_path, monkeypatch):
    module = _load_module()
    source = tmp_path / "source.py"
    source.write_text(
        'CURRENCY_DB = {"XYZ": {"name": "Test Coin", "code": "XYZ", '
        '"symbol": "X", "country": "Testland", "flag": "🏳️", "type": "Fiat"}}'
    )

    fake_repo_root = tmp_path / "repo"
    (fake_repo_root / "data" / "currencies").mkdir(parents=True)
    monkeypatch.setattr(
        module.os.path,
        "abspath",
        lambda p: str(fake_repo_root / "scripts" / "gen_currency_data.py"),
    )

    import sys

    argv_backup = sys.argv
    sys.argv = ["gen_currency_data.py", str(source)]
    try:
        module.main()
    finally:
        sys.argv = argv_backup

    written = fake_repo_root / "data" / "currencies" / "XYZ.json"
    assert written.exists()
    assert json.loads(written.read_text())["name"] == "Test Coin"
