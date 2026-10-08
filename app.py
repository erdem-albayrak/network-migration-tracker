import streamlit as st

st.set_page_config(
    page_title="Network Migration Tracker",
    layout="wide"
)

st.title("Network Migration Project Tracker")
st.caption("Technical Project Management Portfolio — Erdem Albayrak")
st.info("Bu proje, örnek verilerle hazırlanmış bir portföy çalışmasıdır.")

sites = [
    {
        "Site": "Istanbul",
        "Owner": "Engineer A",
        "Planned Date": "2026-10-12",
        "Status": "Completed",
    },
    {
        "Site": "Ankara",
        "Owner": "Engineer B",
        "Planned Date": "2026-10-19",
        "Status": "In Progress",
    },
    {
        "Site": "Izmir",
        "Owner": "Engineer C",
        "Planned Date": "2026-10-26",
        "Status": "Planned",
    },
]

completed = sum(site["Status"] == "Completed" for site in sites)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sites", len(sites))
col2.metric("Completed", completed)
col3.metric("Completion", f"{completed / len(sites):.0%}")

st.subheader("Migration Status")

selected_status = st.selectbox(
    "Filter by status",
    ["All", "Planned", "In Progress", "Completed"],
)

filtered_sites = [
    site for site in sites
    if selected_status == "All" or site["Status"] == selected_status
]

st.caption(
    "Üstteki göstergeler tüm projeyi, tablo seçilen durumdaki lokasyonları gösterir."
)
st.dataframe(filtered_sites, use_container_width=True)