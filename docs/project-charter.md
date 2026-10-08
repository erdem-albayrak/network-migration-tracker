\# Project Charter — Network Migration Tracker



\## 1. Project Purpose

Build a dashboard to track a simulated router migration across

10 branch locations, providing visibility into progress,

ownership, planned dates, risks and issues.



This is a portfolio project using fictional data.

It does not connect to or modify real network devices.



\## 2. Project Owner

Erdem Albayrak — Technical Project Manager / Portfolio Author



\## 3. Business Need

Migration information spread across emails and spreadsheets

can make it difficult to identify delays and track ownership.

The dashboard will provide a central view of migration status.



\## 4. Objectives

\- Track migration progress across 10 sample locations.

\- Assign an owner and planned migration date to each location.

\- Filter locations by migration status.

\- Identify overdue, incomplete migrations.

\- Record risks and issues with owners and actions.

\- Export migration status as a CSV report.



\## 5. Scope



\### In Scope

\- Python and Streamlit dashboard.

\- Fictional migration data for 10 locations.

\- Status metrics and filtering.

\- Planned dates and overdue indicators.

\- Basic risk and issue register.

\- CSV export.

\- Project documentation and GitHub change history.



\### Out of Scope

\- Real device configuration or automated migration.

\- Live network monitoring.

\- Production deployment.

\- User authentication and enterprise integrations.



\## 6. Deliverables

\- Working dashboard.

\- Sample migration dataset.

\- Project charter.

\- RAID register.

\- Acceptance checklist and test results.

\- README with installation and usage instructions.



\## 7. Milestones

1\. Initial dashboard — completed.

2\. Planned dates and status filtering — implemented;

&#x20;  acceptance testing to be recorded.

3\. Project charter and scope baseline.

4\. Ten-location dataset and overdue indicators.

5\. Risk and issue register.

6\. CSV export, final testing and documentation.



\## 8. Acceptance Criteria

\- The dashboard runs locally using documented instructions.

\- All 10 sample locations are displayed when "All" is selected.

\- Each status filter displays only matching locations.

\- Summary metrics accurately reflect the complete dataset.

\- Each location has an owner and a planned migration date.

\- An incomplete migration is overdue when its planned date

&#x20; is earlier than the current date.

\- Completed migrations are not flagged as overdue.

\- Risks and issues include an owner and a response action.

\- CSV export contains the currently filtered migration rows.

\- No credentials or real customer data are stored in the repository.



\## 9. Initial Risks and Responses

\- Scope growth: deliver the agreed features before adding extras.

\- Package compatibility: record dependencies and verify installation.

\- Data loss: commit and push completed changes regularly.

\- Incorrect metrics: test calculations against known sample data.



\## 10. Assumptions and Constraints

\- The project is developed by one person with AI assistance.

\- Stakeholder roles and migration scenarios are simulated.

\- The application runs locally on Windows.

\- No paid cloud services or production infrastructure are required.



\## 11. Change Control

Record new requirements as GitHub issues.

Assess their impact on scope, effort and acceptance criteria.

Implement changes on separate branches and review them through

pull requests before merging into main.

