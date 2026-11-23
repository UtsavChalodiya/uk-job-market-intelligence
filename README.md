# UK Job Market Intelligence

An end-to-end data analytics project exploring the UK data-job market using job listings from the Reed Jobseeker API. The goal is to turn raw vacancy data into a structured dataset that can be analysed with SQL and presented in Power BI.

## Business questions

- Which data roles appear most frequently in the collected listings?
- How do advertised salary ranges vary by role and location?
- How do permanent and contract opportunities differ?
- How does the mix of advertised roles change over time?

**Scope note:** The current ingestion workflow searches for data analyst, data engineer and data scientist roles. Skill extraction and a complete month-by-month trend analysis are potential extensions, not claims made by the current pipeline.

## Technology

- Python: API ingestion and data preparation
- PostgreSQL: persistent storage and SQL analysis
- SQL: cleaning views and analytical queries
- Power BI: planned dashboard layer

## Data pipeline

`Reed API → data/raw/jobs.json → jobs_raw (PostgreSQL) → jobs_clean view → SQL analysis → Power BI`

The repository has previously recorded 528 downloaded listings and 397 unique job IDs. These are historical collection counts, not a live count; rerun the pipeline to refresh the dataset.

## Project structure

- `src/fetch_reed.py` — retrieves listings from the Reed API
- `src/load.py` — loads the collected records into PostgreSQL
- `src/analyze.py` — runs the SQL statements in `sql/analysis.sql`
- `src/analyze_clean.py` — creates the cleaned view and prints summary queries
- `sql/schema.sql` — creates the raw jobs table
- `sql/clean_view.sql` — defines the cleaned analytical view
- `data/raw/jobs.json` — local API response data (created by the fetch script)

## Setup

1. Clone the repository and create a virtual environment:

   ```bash
   git clone https://github.com/UtsavChalodiya/uk-job-market-intelligence.git
   cd uk-job-market-intelligence
   python -m venv .venv
   ```

2. Activate the environment and install dependencies:

   ```bash
   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set your own credentials:

   ```dotenv
   REED_API_KEY=your_reed_api_key
   DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require
   ```

   Never commit `.env` or paste API keys into source code. The Reed API key must be obtained from Reed and the database URL must point to a PostgreSQL database you control.

4. Run the pipeline from the repository root:

   ```bash
   python src/fetch_reed.py
   python src/load.py
   python src/analyze_clean.py
   ```

   `src/analyze.py` runs the separate SQL script in `sql/analysis.sql`.

## Data and interpretation notes

- Salary comparisons should use comparable annual salary values and clearly state any filters.
- Job-advert salary ranges are advertised figures, not necessarily salaries offered or accepted.
- Listings are a snapshot of the API at collection time and may contain duplicates, incomplete salary data or inconsistent job titles.
- The current SQL cleaning view filters job titles and derives a midpoint from minimum and maximum salary. It does not yet extract individual skills from descriptions.

## Current status

The Python ingestion and PostgreSQL/SQL workflow is represented in the repository. The Power BI dashboard is still in progress; dashboard screenshots and final findings will be added when that work is complete.

## Author

**Utsav Chalodiya**  
[GitHub profile](https://github.com/UtsavChalodiya)
