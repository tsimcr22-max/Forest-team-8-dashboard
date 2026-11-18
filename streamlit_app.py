"""The dashboard's screens. Run it with:  streamlit run streamlit_app.py

This page is the template's starting point. It proves the app reads your
team's database, and it is what the roadmap's hello-world deploy puts
online. Replace it with the screens your spec describes and design.md draws;
keep every query in dashboard/metrics.py and draw every chart with
dashboard/charts.py.

Rule for a public app on a shared login: no box where a viewer can type SQL.
Filters (dropdowns, sliders, dates) pass values to the queries as parameters.
"""

import streamlit as st

from dashboard import db, metrics

st.set_page_config(page_title="Dashboard", layout="wide")


# Cached for ten minutes: every viewer shares one answer instead of each
# sending the same query to the server.
@st.cache_data(ttl=600)
def load_about():
    return metrics.about(db.get_engine())


st.title("Dashboard")

about = load_about()
st.success(f"Connected to **{about.loc[0, 'display_name']}**: {about.loc[0, 'description']}")
st.info("Your database is connected. Build the screens spec.md describes and design.md draws.")
