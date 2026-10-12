from datetime import date
from pathlib import Path
from html import escape

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

required_progress = ["Progress Notes", "Next Actions", "Last Updated"]
missing = [column for column in required_progress if column not in df.columns]
if missing:
    st.error("Yeni migrations.csv dosyasını data klasörüne koyun. Eksik sütunlar: " + ", ".join(missing))
    st.stop()
tasks = pd.read_csv(data_path.parent / "tasks.csv").fillna("")
required_tasks = ["Task ID", "Site", "Task", "Phase", "Owner", "Start Date", "End Date", "Status", "Depends On", "Waiting Reason", "Actual Finish"]
if any(column not in tasks for column in required_tasks):
    st.error("tasks.csv sütunları eksik.")
    st.stop()
if tasks["Task ID"].duplicated().any() or not tasks["Site"].isin(df["Site"]).all() or df["Site"].duplicated().any():
    st.error("Task ID ve Site benzersiz olmalı; görevlerin lokasyonları migrations.csv içinde bulunmalı.")
    st.stop()
if not tasks["Status"].isin(["Planned", "In Progress", "Waiting", "Completed"]).all():
    st.error("Görev durumu Planned, In Progress, Waiting veya Completed olmalı.")
    st.stop()
for column in ["Start Date", "End Date"]:
    tasks[column] = pd.to_datetime(tasks[column], format="%Y-%m-%d", errors="coerce")
if tasks[["Start Date", "End Date"]].isna().any().any() or (tasks["End Date"] < tasks["Start Date"]).any():
    st.error("Görev tarihleri YYYY-MM-DD olmalı; bitiş başlangıçtan önce olamaz.")
    st.stop()
task_ids = set(tasks["Task ID"])
task_sites = tasks.set_index("Task ID")["Site"].to_dict()
dependencies = tasks.set_index("Task ID")["Depends On"].to_dict()
for task_id, predecessor in dependencies.items():
    if predecessor and (predecessor not in task_ids or task_sites[predecessor] != task_sites[task_id]):
        st.error("Bağımlılıklar aynı lokasyondaki geçerli Task ID değerlerini kullanmalı.")
        st.stop()
    visited = {task_id}
    while predecessor:
        if predecessor in visited:
            st.error("Görev bağımlılıklarında döngü var.")
            st.stop()
        visited.add(predecessor)
        predecessor = dependencies.get(predecessor, "")
counts = tasks.groupby("Site").size()
done_counts = tasks[tasks["Status"] == "Completed"].groupby("Site").size()
df["Total Tasks"] = df["Site"].map(counts).fillna(0).astype(int)
df["Completed Tasks"] = df["Site"].map(done_counts).fillna(0).astype(int)
if (df["Total Tasks"] == 0).any():
    st.error("Her lokasyon için tasks.csv içinde en az bir görev olmalı.")
    st.stop()
df["Progress (%)"] = (100 * df["Completed Tasks"] / df["Total Tasks"]).round(1)
df["Tasks Done / Total"] = df["Completed Tasks"].astype(str) + " / " + df["Total Tasks"].astype(str)
for column in ["Progress Notes", "Next Actions", "Last Updated"]:
    df[column] = df[column].fillna("")
inconsistent = ((df["Status"] == "Completed") & (df["Completed Tasks"] != df["Total Tasks"])) | ((df["Status"] == "Planned") & (df["Completed Tasks"] > 0))
if inconsistent.any():
    st.warning("Bazı lokasyonlarda durum ile iş sayıları uyumsuz. Status ve Completed Tasks alanlarını kontrol edin.")

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

task_total = int(df["Total Tasks"].sum())
task_done = int(df["Completed Tasks"].sum())
task_col1, task_col2, task_col3 = st.columns(3)
task_col1.metric("Work Items Completed", f"{task_done} / {task_total}")
task_col2.metric("Work Item Progress", f"{task_done / task_total:.0%}" if task_total else "0%")
task_col3.metric("Remaining Work Items", task_total - task_done)
st.caption("Completion = tamamlanan lokasyon oranı. Work Item Progress = tamamlanan iş / toplam iş; her iş eşit ağırlıklıdır. İş sayıları ve notlar örnek senaryodur.")

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
    display_columns = ["Site", "Owner", "Planned Date", "Status", "Overdue", "Progress Notes", "Next Actions", "Tasks Done / Total", "Progress (%)", "Last Updated"]
    st.dataframe(filtered[display_columns], width="stretch", hide_index=True)
    with st.expander("Site Progress & Meeting Notes", expanded=True):
        selected_site = st.selectbox("Select site for details", filtered["Site"].tolist())
        site = filtered.loc[filtered["Site"] == selected_site].iloc[0]
        st.write(f"**{selected_site} — {site['Status']} | Owner: {site['Owner']}**")
        st.progress(float(site["Progress (%)"]) / 100)
        st.write(f"**Completed work items:** {site['Tasks Done / Total']} ({site['Progress (%)']:g}%)")
        st.write("**Progress Notes**")
        st.write(site["Progress Notes"])
        st.write("**Next Actions**")
        st.write(site["Next Actions"])
        st.caption(f"Last Updated: {site['Last Updated']}")
        st.write("**Migration stages — work items completed**")
        site_tasks = tasks[tasks["Site"] == selected_site].reset_index(drop=True)
        stage_columns = st.columns(5)
        for stage_index, stage_name in enumerate(["Planning", "Readiness", "Execution", "Validation", "Acceptance"]):
            stage_tasks = site_tasks[site_tasks["Phase"] == stage_name]
            stage_done = int((stage_tasks["Status"] == "Completed").sum())
            stage_columns[stage_index].metric(stage_name, f"{stage_done} / {len(stage_tasks)}")
        st.caption("Aşama kutuları tasks.csv içindeki Phase alanından hesaplanır: Planning, Readiness, Execution, Validation, Acceptance.")
    st.caption("İş sayıları tasks.csv üzerinden hesaplanır. Görev durumlarını tasks.csv; lokasyon durumu ve toplantı notlarını migrations.csv üzerinden güncelleyin. Sayfayı yenileyin.")
st.download_button(
    label="Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name=f"migration_report_{today:%Y-%m-%d}.csv",
    mime="text/csv",
    disabled=filtered.empty,
)
st.divider()
st.subheader("RAID Register")
st.caption("Risks, Assumptions, Issues and Dependencies — fictional portfolio data.")

raid_path = Path(__file__).parent / "data" / "raid.csv"
raid_df = pd.read_csv(raid_path)

raid_type = st.selectbox(
    "Filter RAID by type",
    ["All", "Risk", "Assumption", "Issue", "Dependency"],
)

raid_filtered = raid_df.copy()

if raid_type != "All":
    raid_filtered = raid_filtered[raid_filtered["Type"] == raid_type]

st.dataframe(
    raid_filtered,
    width="stretch",
    hide_index=True,
)

st.download_button(
    label="Download filtered RAID as CSV",
    data=raid_filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name=f"raid_report_{today:%Y-%m-%d}.csv",
    mime="text/csv",
    disabled=raid_filtered.empty,
)

st.divider()
st.subheader("Project Visual Overview")
left, right = st.columns(2)
with left:
    st.write("**Work item progress by site (%)**")
    st.bar_chart(df.set_index("Site")[["Progress (%)"]])
with right:
    st.write("**Migration status distribution**")
    st.bar_chart(df["Status"].value_counts().rename("Sites"))
st.caption("Grafikler tüm projeyi gösterir. Örnek iş sayıları eşit ağırlıklıdır; maliyet veya efor ağırlıklı ilerleme değildir.")

st.subheader("Gantt Timeline & Daily Actions")
view_date = st.date_input("Review date", value=today)
timeline_site = st.selectbox("Gantt site", ["All"] + df["Site"].tolist())
scope = tasks if timeline_site == "All" else tasks[tasks["Site"] == timeline_site]
open_tasks = scope[scope["Status"] != "Completed"].copy()
status_by_id = tasks.set_index("Task ID")["Status"].to_dict()
open_tasks["Predecessor Open"] = open_tasks["Depends On"].apply(lambda x: bool(x) and status_by_id.get(x) != "Completed")
review = pd.Timestamp(view_date)
today_tasks = open_tasks[(open_tasks["Start Date"] <= review) & (open_tasks["End Date"] >= review)]
late_tasks = open_tasks[open_tasks["End Date"] < review]
blocked_tasks = open_tasks[(open_tasks["Status"] == "Waiting") | open_tasks["Predecessor Open"]]
for label, subset in [("Today / Review Date", today_tasks), ("Overdue Work Items", late_tasks), ("Waiting / Dependency Blocked", blocked_tasks)]:
    with st.expander(f"{label} ({len(subset)})"):
        st.dataframe(subset, hide_index=True, width="stretch")
st.caption("Listeler çakışabilir: bir görev hem gecikmiş hem bağımlılık nedeniyle bekliyor olabilir. Review date bu bölümü ve kilometre taşlarını etkiler; üstteki gecikme göstergesi bugünü kullanır.")

def gantt_svg(frame, review_date):
    origin = min(frame["Start Date"].min().normalize(), pd.Timestamp(review_date))
    finish = max(frame["End Date"].max().normalize(), pd.Timestamp(review_date)) + pd.Timedelta(days=1)
    days = max(1, (finish-origin).days)
    scale = max(24, min(55, 900/days))
    label_width = 350
    width = label_width + days*scale + 30
    height = 65 + len(frame)*27
    colors = {"Completed":"#16a34a", "In Progress":"#2563eb", "Waiting":"#d97706", "Planned":"#94a3b8"}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="Gantt task timeline">', f'<rect width="{width}" height="{height}" fill="#f8fafc"/>']
    for d in range(days):
        x=label_width+d*scale
        label=(origin+pd.Timedelta(days=d)).strftime("%d %b")
        parts.append(f'<line x1="{x}" y1="45" x2="{x}" y2="{height}" stroke="#e2e8f0"/><text x="{x+2}" y="30" font-size="10" fill="#334155">{label}</text>')
    for i,(_,row) in enumerate(frame.iterrows()):
        y=55+i*27
        x=label_width+(row["Start Date"].normalize()-origin).days*scale
        bar=max(scale-3, ((row["End Date"].normalize()-row["Start Date"].normalize()).days+1)*scale-3)
        label=escape(f"{row['Task ID']} {row['Task']}")
        tooltip=escape(f"{row['Site']} | {row['Status']} | {row['Owner']}")
        parts.append(f'<text x="8" y="{y+14}" font-family="sans-serif" font-size="11" fill="#0f172a">{label}</text><rect x="{x}" y="{y}" width="{bar}" height="19" rx="4" fill="{colors[row["Status"]]}"><title>{tooltip}</title></rect>')
    x=label_width+(pd.Timestamp(review_date)-origin).days*scale
    if label_width <= x <= width-30:
        parts.append(f'<line x1="{x}" y1="40" x2="{x}" y2="{height}" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 3"/>')
    return ''.join(parts)+'</svg>'

st.caption("Yeşil: Completed · Mavi: In Progress · Turuncu: Waiting · Gri: Planned · Kırmızı çizgi: review date. Çubuklar planlanan tarihleri gösterir.")
gantt_detail = st.selectbox("Timeline detail site", scope["Site"].unique().tolist())
chart_tasks = scope[scope["Site"] == gantt_detail]
st.markdown('<div style="overflow-x:auto">'+gantt_svg(chart_tasks, view_date)+'</div>', unsafe_allow_html=True)
st.dataframe(scope, hide_index=True, width="stretch")
st.download_button("Download task plan", scope.to_csv(index=False, date_format="%Y-%m-%d").encode("utf-8-sig"), file_name="task_plan.csv", mime="text/csv")

st.subheader("Milestone Tracker")
milestones = pd.read_csv(data_path.parent / "milestones.csv").fillna("")
if not milestones["Task ID"].isin(task_ids).all():
    st.error("Kilometre taşlarında geçersiz Task ID var.")
    st.stop()
milestones["Target Date"] = pd.to_datetime(milestones["Target Date"], format="%Y-%m-%d")
milestones["Status"] = milestones["Task ID"].map(status_by_id)
milestones["Overdue"] = (milestones["Target Date"] < review) & (milestones["Status"] != "Completed")
st.dataframe(milestones, hide_index=True, width="stretch")
st.caption("Kilometre taşı durumu bağlantılı görevin durumundan hesaplanır. Target Date, onaylı hedef tarihtir.")

st.subheader("Change Log")
changes = pd.read_csv(data_path.parent / "changes.csv").fillna("")
st.dataframe(changes, hide_index=True, width="stretch")
st.caption("Örnek talepler Pending durumundadır. Onaylanmadan plan tarihleri değiştirilmez; onay sonrası etkilenen görev ve hedef tarihleri ayrıca güncellenir.")

st.subheader("Meeting Focus")
st.write(f"**Delivery:** {completed}/{total} sites accepted; {task_done}/{task_total} work items completed.")
st.write(f"**Schedule:** {overdue} sites past planned migration date; {len(late_tasks)} open work items past review date in the selected Gantt scope.")
st.write(f"**RAID:** {len(raid_df[~raid_df['Status'].isin(['Closed', 'Completed', 'Resolved'])])} active records; review owners and actions.")
st.write("**Decisions:** Resolve configuration mismatch, obtain customer acceptance, confirm carrier activation and equipment readiness.")
st.caption("Son karar başlıkları örnek toplantı gündemidir; canlı veriye göre migrations.csv içindeki Next Actions alanlarını gözden geçirin.")


st.divider()
st.header("Programme Toolkit")
st.info("Excel referans senaryosu: 24 şube, 2 core site, IP/MPLS dönüşümü. Bu bölüm mevcut 10 lokasyon / 200 görev senaryosundan bağımsızdır. Maliyetler örnek USD değerleridir.")
report_date = st.date_input("Programme reporting date", value=date(2026, 10, 2))
report_ts = pd.Timestamp(report_date)
def toolkit_csv(name):
    return pd.read_csv(data_path.parent / (name + ".csv")).fillna("")
def toolkit_dates(frame, columns):
    for column in columns:
        frame[column] = pd.to_datetime(frame[column], format="%Y-%m-%d", errors="coerce")
    return frame
plan = toolkit_dates(toolkit_csv("programme_plan"), ["Baseline start", "Baseline finish", "Actual finish", "Forecast finish"])
budget = toolkit_csv("budget")
resources = toolkit_csv("resources")
risks = toolkit_dates(toolkit_csv("programme_raid"), ["Due date"])
actions = toolkit_dates(toolkit_csv("actions"), ["Due date"])
programme_milestones = toolkit_dates(toolkit_csv("programme_milestones"), ["Baseline", "Forecast", "Actual"])
decisions = toolkit_dates(toolkit_csv("decisions"), ["Required By"])
for column in ["Complete", "Effort days"]:
    plan[column] = pd.to_numeric(plan[column], errors="coerce")
if plan[["Complete", "Effort days"]].isna().any().any() or not plan["Complete"].between(0, 1).all() or (plan["Effort days"] <= 0).any():
    st.error("Programme plan: Complete 0–1, Effort days sıfırdan büyük olmalı.")
    st.stop()
if plan[["Baseline start", "Baseline finish", "Forecast finish"]].isna().any().any() or (plan["Baseline finish"] < plan["Baseline start"]).any():
    st.error("Programme plan tarihlerini kontrol edin.")
    st.stop()
plan["Weighted effort"] = plan["Complete"] * plan["Effort days"]
plan["Slip days"] = (plan["Actual finish"].fillna(plan["Forecast finish"]) - plan["Baseline finish"]).dt.days
for column in ["Approved budget", "Planned to date", "Actual to date", "Remaining forecast"]:
    budget[column] = pd.to_numeric(budget[column], errors="coerce")
if budget[["Approved budget", "Planned to date", "Actual to date", "Remaining forecast"]].isna().any().any() or (budget[["Approved budget", "Planned to date", "Actual to date", "Remaining forecast"]] < 0).any().any():
    st.error("Budget alanları negatif olmayan sayılar olmalı.")
    st.stop()
budget["Forecast at completion"] = budget["Actual to date"] + budget["Remaining forecast"]
budget["Variance USD"] = budget["Forecast at completion"] - budget["Approved budget"]
budget["Variance %"] = (100 * budget["Variance USD"] / budget["Approved budget"].replace(0, float("nan"))).round(1)
for column in ["Capacity days", "Assigned days"]:
    resources[column] = pd.to_numeric(resources[column], errors="coerce")
if resources[["Capacity days", "Assigned days"]].isna().any().any() or (resources["Capacity days"] <= 0).any() or (resources["Assigned days"] < 0).any():
    st.error("Capacity days sıfırdan büyük, Assigned days negatif olmayan sayı olmalı.")
    st.stop()
resources["Utilization %"] = (100 * resources["Assigned days"] / resources["Capacity days"]).round(1)
resources["Gap days"] = (resources["Assigned days"] - resources["Capacity days"]).clip(lower=0)
is_risk = risks["Type"] == "Risk"
probability = pd.to_numeric(risks["Probability 1–5"], errors="coerce")
impact = pd.to_numeric(risks["Impact 1–5"], errors="coerce")
risks["Probability 1–5"] = probability.astype("Float64")
risks["Impact 1–5"] = impact.astype("Float64")
if not probability[is_risk].between(1,5).all() or not impact[is_risk].between(1,5).all():
    st.error("Risk Probability ve Impact değerleri 1–5 aralığında olmalı.")
    st.stop()
risks["Risk score"] = (probability * impact).where(is_risk)
active_risks = ~risks["Status"].isin(["Closed", "Resolved", "Completed"])
risks["High open risk"] = is_risk & active_risks & (risks["Risk score"] >= 15)
risks["Overdue"] = active_risks & (risks["Due date"] < report_ts)
actions["Overdue"] = ~actions["Status"].isin(["Closed", "Completed", "Resolved"]) & (actions["Due date"] < report_ts)
decisions["Overdue"] = (decisions["Status"] == "Pending") & (decisions["Required By"] < report_ts)
programme_milestones["Slip days"] = (programme_milestones["Actual"].fillna(programme_milestones["Forecast"]) - programme_milestones["Baseline"]).dt.days
programme_milestones["Status"] = programme_milestones.apply(lambda r: "Complete" if pd.notna(r["Actual"]) else "Red" if r["Slip days"] > 14 else "Amber" if r["Slip days"] > 0 else "Green", axis=1)
approved = float(budget["Approved budget"].sum())
forecast = float(budget["Forecast at completion"].sum())
variance = forecast - approved
closure = plan.loc[plan["ID"] == "T12"]
if len(closure) != 1 or approved <= 0:
    st.error("Programme plan tek T12 kapanış görevi ve pozitif toplam bütçe içermeli.")
    st.stop()
closure_slip = int(closure["Slip days"].iloc[0])
overall_rag = "Red" if closure_slip > 14 else "Amber" if closure_slip > 0 or variance/approved > .05 else "Green"
weighted_progress = float(plan["Weighted effort"].sum()/plan["Effort days"].sum())
tab_summary, tab_plan, tab_budget, tab_people, tab_risks, tab_actions = st.tabs(["Programme Status", "Baseline & Forecast", "Budget", "Resources & RACI", "Risk Matrix", "Actions & Decisions"])
with tab_summary:
    cols=st.columns(4)
    cols[0].metric("Overall RAG", overall_rag)
    cols[1].metric("Effort-weighted progress", f"{weighted_progress:.1%}")
    cols[2].metric("Closure slip (days)", closure_slip)
    cols[3].metric("Budget variance", f"{variance/approved:.1%}")
    st.caption("Excel yöntemi: kapanış kayması >14 gün Red; herhangi bir kapanış kayması veya bütçe aşımı >%5 Amber; aksi Green. Kapsam/kalite için PM değerlendirmesi ayrıca gerekir.")
    st.write(f"High open risks: **{int(risks['High open risk'].sum())}** · Resource gap: **{resources['Gap days'].sum():g} engineer days** · Overdue actions: **{int(actions['Overdue'].sum())}**")
    st.dataframe(decisions, hide_index=True, width="stretch")
with tab_plan:
    st.caption("Complete: 0–1 arası ilerleme. Ağırlıklı ilerleme = Σ(Complete × Effort days) / Σ(Effort days). Slip takvim günü olarak gerçekleşen veya tahmin edilen bitiş eksi baseline bitiştir.")
    st.dataframe(plan, hide_index=True, width="stretch")
    st.bar_chart(plan.set_index("Task")[["Slip days"]])
    st.write("**Programme milestones: baseline / forecast / actual**")
    st.dataframe(programme_milestones, hide_index=True, width="stretch")
with tab_budget:
    cols=st.columns(3)
    cols[0].metric("Approved USD", f"{approved:,.0f}")
    cols[1].metric("Forecast USD", f"{forecast:,.0f}")
    cols[2].metric("Forecast overspend USD", f"{variance:,.0f}")
    st.bar_chart(budget.set_index("Category")[["Approved budget", "Actual to date", "Forecast at completion"]])
    st.dataframe(budget, hide_index=True, width="stretch")
    st.caption("Forecast = actual + kalan maliyet tahmini. Pozitif variance bütçe aşımıdır. Contingency toplam bütçeye dahildir; sıfır bütçeli kategoride yüzde hesaplanmaz.")
with tab_people:
    st.caption("Kaynak planı Ekim 2026 dönemi içindir; reporting date değiştirilmesi kapasite dönemini değiştirmez.")
    st.bar_chart(resources.set_index("Role")[["Capacity days", "Assigned days"]])
    st.dataframe(resources, hide_index=True, width="stretch")
    raci = toolkit_csv("raci")
    accountable = raci.iloc[:,1:].apply(lambda row: sum("A" in str(v).split("/") for v in row), axis=1)
    if (accountable != 1).any():
        st.warning("RACI: Her faaliyet için tam bir Accountable rolü olmalı.")
    st.write("**RACI responsibility matrix**")
    st.dataframe(raci, hide_index=True, width="stretch")
    st.caption("R: işi yapan · A: nihai hesap veren/onaylayan · C: görüşü alınan · I: bilgilendirilen.")
with tab_risks:
    grid = [[0]*5 for _ in range(5)]
    for index in risks.index[is_risk & active_risks]:
        grid[int(impact[index])-1][int(probability[index])-1] += 1
    colors=["#dcfce7", "#fef3c7", "#fee2e2"]
    html='<table style="border-collapse:collapse;color:#0f172a"><tr><th style="padding:10px">Impact / Probability</th>'+''.join(f'<th style="padding:10px">{p}</th>' for p in range(1,6))+'</tr>'
    for i in range(5,0,-1):
        html+=f'<tr><th style="padding:10px">{i}</th>'
        for p in range(1,6):
            score=i*p; color=colors[2] if score>=15 else colors[1] if score>=8 else colors[0]
            html+=f'<td style="padding:15px;background:{color};border:1px solid white;text-align:center">{grid[i-1][p-1]} risk</td>'
        html+='</tr>'
    st.markdown(html+'</table>', unsafe_allow_html=True)
    st.caption("Hücreler açık risk sayısını gösterir. Puan = olasılık × etki; ≥15 yüksek, 8–14 orta, <8 düşük. Issue/Assumption/Dependency kayıtlarına risk puanı verilmez.")
    st.dataframe(risks, hide_index=True, width="stretch")
with tab_actions:
    st.write("**Action log**")
    st.dataframe(actions, hide_index=True, width="stretch")
    st.write("**Decision log**")
    st.dataframe(decisions, hide_index=True, width="stretch")
    st.caption("Reference, Excel senaryosundaki RAID/karar/kilometre taşı ID değerlerine bağlanır; migration senaryosunun ID değerlerinden farklıdır.")
st.caption("Programme Toolkit girdileri data/programme_*.csv, budget.csv, resources.csv, raci.csv, actions.csv ve decisions.csv dosyalarında güncellenir. Excel'deki 02-Oct-2026 raporu başlangıç referansıdır; reporting date seçimi tarih tabanlı gecikmeleri yeniden hesaplar, ilerlemeyi kendiliğinden değiştirmez.")
