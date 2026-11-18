# Dashboard Template

A template for a Streamlit dashboard on the course PostgreSQL server: the
connection already set up for Streamlit Community Cloud, a data layer, and a
test suite.

**Live app:** <paste your Community Cloud link here>

---

## Start a project from it

On GitHub, **Use this template → Create a new repository**, or ask Claude Code:

> *"Create a **public** GitHub repository called `<section>-team-<n>-dashboard` from the template `wfu-martin/dashboard-template`, and clone it here."*

## Run it on your laptop

```bash
conda create -n dashboard python=3.12 -y
conda activate dashboard
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then fill in the password
streamlit run streamlit_app.py
```

## Test it

```bash
pytest
```

The connection tests run anywhere. The database tests skip until
`.streamlit/secrets.toml` exists, and `tests/test_connection.py` fails until
`database` names your team's database.

## Deploy it on Streamlit Community Cloud

You do this once, during the roadmap's hello-world deploy task; `/dashkit:build-next` walks you through it. After that, every merge to `main` redeploys the app.

1. At [share.streamlit.io](https://share.streamlit.io), **Create app** → **Deploy a public app from GitHub**.
2. Pick this repository, branch `main`, main file `streamlit_app.py`.
3. **Advanced settings:** Python 3.12, and paste the contents of your `secrets.toml` into **Secrets**.
4. Deploy, then paste the app's link at the top of this README.

## What is where

| Path | What it is |
|---|---|
| `streamlit_app.py` | The screens |
| `dashboard/db.py` | Every connection setting, and why |
| `dashboard/metrics.py` | One function per figure on screen |
| `dashboard/charts.py` | Headlines, number tiles, and charts in the house style |
| `.streamlit/config.toml` | The app's colors and font |
| `tools/progress.py` | The two-line progress tracker the skills show |
| `tests/` | The tests; `test_connection.py` proves the app reads your database |
| `briefs/stakeholder-email.md` | Your stakeholder brief: one person, one decision, exactly 4 high-level business questions. Start the spec with `/dashkit:spec briefs/stakeholder-email.md` |
| `spec.md` | What to build (written with `/dashkit:spec`) |
| `design.md` | Each screen as drawn, and the style rules (screens drawn with `/dashkit:design`) |
| `mockup.py` | The screens with made-up numbers, for sign-off before building (`streamlit run mockup.py`) |
| `ROADMAP.md` | Phases and critical path (written with `/dashkit:roadmap`) |
| `ROLES.md` | Who owns what |
| `CLAUDE.md` | What Claude Code reads at the start of every session |
