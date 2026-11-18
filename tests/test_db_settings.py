"""The connection settings, checked without touching the database.

These run anywhere, even before you have a password. They pin the settings
that keep the app working on Streamlit Community Cloud and keep the class
inside the server's connection limit.
"""

from pathlib import Path

import certifi
import pytest

from dashboard import db

ROOT = Path(__file__).resolve().parent.parent


def test_tls_is_verify_full_with_certifi_roots():
    args = db.connect_args()
    assert args["sslmode"] == "verify-full"
    assert args["sslrootcert"] == certifi.where()
    assert Path(args["sslrootcert"]).is_file()


def test_pool_survives_idle_timeout():
    # The server closes a connection left idle for 30 minutes.
    assert db.ENGINE_OPTIONS["pool_pre_ping"] is True
    assert db.ENGINE_OPTIONS["pool_recycle"] < 30 * 60


def test_pool_is_small():
    # Every laptop and every deployed app shares one connection limit.
    assert db.ENGINE_OPTIONS["pool_size"] + db.ENGINE_OPTIONS["max_overflow"] <= 3


def test_engine_from_secrets_builds_url(tmp_path):
    secrets = tmp_path / "secrets.toml"
    secrets.write_text(
        "[connections.db]\n"
        'dialect = "postgresql"\n'
        'driver = "psycopg"\n'
        'host = "example.org"\n'
        "port = 5432\n"
        'database = "tucana"\n'
        'username = "student"\n'
        'password = "not-a-real-password"\n'
    )
    engine = db.engine_from_secrets(secrets)
    assert engine.url.drivername == "postgresql+psycopg"
    assert engine.url.host == "example.org"
    assert engine.url.database == "tucana"
    assert engine.pool.size() == db.ENGINE_OPTIONS["pool_size"]
    assert engine.pool.checkedout() == 0  # nothing was opened
    engine.dispose()


def test_missing_secrets_file_says_what_to_do(tmp_path):
    with pytest.raises(FileNotFoundError, match=r"secrets\.toml\.example"):
        db.engine_from_secrets(tmp_path / "secrets.toml")


def test_placeholder_password_never_reaches_the_server(tmp_path):
    # A wrong password counts toward the server's lockout, and a classroom
    # shares one address: refuse before connecting, and say what to do.
    secrets = tmp_path / "secrets.toml"
    secrets.write_text(
        "[connections.db]\n"
        'dialect = "postgresql"\n'
        'driver = "psycopg"\n'
        'host = "example.invalid"\n'
        'database = "tucana"\n'
        'username = "student"\n'
        f'password = "{db.PASSWORD_PLACEHOLDER}"\n'
    )
    with pytest.raises(ValueError, match="paste the student password"):
        db.engine_from_secrets(secrets)


def test_app_with_placeholder_password_asks_for_it_without_connecting(tmp_path, monkeypatch):
    from streamlit.testing.v1 import AppTest

    # A fresh copy of the example, password not yet pasted, in an empty folder
    # so a real .streamlit/secrets.toml is never read.
    (tmp_path / ".streamlit").mkdir()
    example = (ROOT / ".streamlit" / "secrets.toml.example").read_text()
    (tmp_path / ".streamlit" / "secrets.toml").write_text(
        example.replace('host = "datalake.databasevoyager.com"', 'host = "example.invalid"')
    )
    monkeypatch.chdir(tmp_path)
    app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=10).run()
    assert not app.exception
    assert "paste the student password" in app.error[0].value
