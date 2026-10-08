\# Network Migration Tracker



A technical project management portfolio application built with Python, Streamlit, and pandas.



The project simulates tracking a network migration across 10 sites, combining delivery progress, overdue visibility, and RAID management.



\## Features



\- Load migration records from a CSV file.

\- Display total sites, completed sites, completion percentage, and overdue count.

\- Filter migrations by status.

\- Show overdue migrations only.

\- Download the filtered migration table as CSV.

\- Track risks, assumptions, issues, and dependencies in a RAID register.

\- Filter RAID records by type.

\- Download the filtered RAID register as CSV.



\## Project Management Approach



\- Project scope and objectives documented in a project charter.

\- Migration records include an owner, planned date, and status.

\- RAID records include an owner, priority, due date, status, and action.

\- Changes developed on separate Git branches and merged through pull requests.



\## Migration Rules



A migration is overdue when its planned date is earlier than the computer's current date and its status is not Completed.



Tested migrations are not considered completed until acceptance and closure.



Dashboard metrics always represent all migration records. Filters apply to the table and its CSV export.



The completion percentage represents completed sites divided by total sites. It does not measure effort or task-level progress.



\## Project Structure



\- `app.py` — Streamlit application

\- `requirements.txt` — Python dependencies

\- `data/migrations.csv` — Fictional migration records

\- `data/raid.csv` — Fictional RAID records

\- `docs/project-charter.md` — Project charter



\## Run Locally on Windows



Run each command separately in Command Prompt.



Clone the repository:



```text

git clone https://github.com/erdem-albayrak/network-migration-tracker.git

```



Open the project folder:



```text

cd network-migration-tracker

```



Create a virtual environment:



```text

python -m venv .venv

```



Activate it:



```text

.venv\\Scripts\\activate

```



Install dependencies:



```text

python -m pip install -r requirements.txt

```



Start the application:



```text

python -m streamlit run app.py

```



Open the local URL displayed in the terminal, usually http://localhost:8501.



Access to the repository is required if it is private.



\## Sample Data and Limitations



All sites, owners, and RAID scenarios are fictional portfolio examples.



The application reads local CSV files. It does not connect to network devices, execute migrations, or update source records through the interface.



Overdue counts change with the current date.



\## Author



Erdem Albayrak

