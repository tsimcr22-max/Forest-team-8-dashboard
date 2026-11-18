"""The repository reads your team's own database.

These skip until .streamlit/secrets.toml exists. Once it does, the first
test fails until `database` names your team's database instead of the
template's placeholder, and the second proves the server answers.
"""

from dashboard.metrics import about

PLACEHOLDER = "PASTE-YOUR-TEAM-DATABASE-HERE"


def test_database_is_named(engine):
    assert engine.url.database != PLACEHOLDER, (
        "Set `database` in .streamlit/secrets.toml to your team's database"
    )


def test_database_describes_itself(engine):
    assert len(about(engine)) == 1
