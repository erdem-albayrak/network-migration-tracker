from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Network Migration Tracker",
    layout="wide"
)

st.title("Network Migration Project Tracker")
st.caption("Technical Project Management Portfolio — Erdem Albayrak")
st.info("Bu proje, örnek verilerle hazırlanmış bir portföy çalışmasıdır.")

data_path = Path(__file__).parent / "data" / "migrations.csv"
df = pd.read_csv(data_path)

df["Planned Date"] = pd.to_datetime(
    df["Planned Date"], format="%Y-%m-%d"
).dt.date

today = date.today()
df["Overdue"] = (
    (df["Planned Date"] < today)
    & (df["Status"] != "Completed")
)

total = len(df)
completed = int((df["Status"] == "Completed").sum())
overdue = int(df["Overdue"].sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sites", total)
col2.metric("Completed", completed)
col3.metric("Completion", f"{completed / total:.0%}" if total else "0%")
col4.metric("Overdue", overdue)

st.caption(f"Gecikme kontrol tarihi: {today:%Y-%m-%d}")
st.subheader("Migration Status")

selected_status = st.selectbox(
    "Filter by status",
    ["All", "Planned", "In Progress", "Tested", "Completed"],
)
only_overdue = st.checkbox("Show overdue migrations only")

filtered = df.copy()

if selected_status != "All":
    filtered = filtered[filtered["Status"] == selected_status]

if only_overdue:
    filtered = filtered[filtered["Overdue"]]

st.caption(
    "Üstteki göstergeler tüm projeyi, tablo seçilen filtreleri gösterir. "
    "Tested durumundaki geçişler henüz tamamlanmış sayılmaz."
)

if filtered.empty:
    st.info("Seçilen filtrelere uygun lokasyon bulunamadı.")
else:
    st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button(
    label="Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name=f"migration_report_{today:%Y-%m-%d}.csv",
    mime="text/csv",
    disabled=filtered.empty,
)