import importlib.util
import json
import os

import pytest

_SCRIPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "scripts",
    "check_currency_data.py",
)


def _load_module():
    spec = importlib.util.spec_from_file_location("check_currency_data", _SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def test_passes_on_the_real_data_directory(capsys):
    module = _load_module()
    module.main()  # does not raise / exit when the real data is valid
    assert "OK" in capsys.readouterr().out


def test_fails_on_missing_field(tmp_path, monkeypatch):
    module = _load_module()
    _write(
        tmp_path / "USD.json",
        {
            "name": "US Dollar",
            "code": "USD",
            "symbol": "$",
            "country": "US",
            "flag": "🇺🇸",
        },
    )
    monkeypatch.setattr(module, "DATA_DIR", str(tmp_path))

    with pytest.raises(SystemExit) as exc:
        module.main()
    assert exc.value.code == 1


def test_fails_when_code_does_not_match_filename(tmp_path, monkeypatch):
    module = _load_module()
    _write(
        tmp_path / "USD.json",
        {
            "name": "US Dollar",
            "code": "WRONG",
            "symbol": "$",
            "country": "US",
            "flag": "🇺🇸",
            "type": "Fiat",
        },
    )
    monkeypatch.setattr(module, "DATA_DIR", str(tmp_path))

    with pytest.raises(SystemExit) as exc:
        module.main()
    assert exc.value.code == 1
