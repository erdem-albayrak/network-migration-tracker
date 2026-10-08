import streamlit as st

st.set_page_config(
    page_title="Network Migration Tracker",
    layout="wide"
)

st.title("Network Migration Project Tracker")
st.caption("Technical Project Management Portfolio — Erdem Albayrak")
st.info("Bu proje, örnek verilerle hazırlanmış bir portföy çalışmasıdır.")

sites = [
    {"Site": "Istanbul", "Owner": "Engineer A", "Status": "Completed"},
    {"Site": "Ankara", "Owner": "Engineer B", "Status": "In Progress"},
    {"Site": "Izmir", "Owner": "Engineer C", "Status": "Planned"},
]

completed = sum(site["Status"] == "Completed" for site in sites)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sites", len(sites))
col2.metric("Completed", completed)
col3.metric("Completion", f"{completed / len(sites):.0%}")

st.subheader("Migration Status")
st.dataframe(sites, use_container_width=True)