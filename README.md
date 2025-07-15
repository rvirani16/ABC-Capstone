## ABC Supply Capstone Project - Analytics for Enhanced Product Understanding

This repository houses the capstone project conducted by UW Madison CDIS students for ABC Supply. Our objective is to leverage ABC Supply's existing analytical tool/product data to generate actionable insights and recommendations through a comprehensive analytical product project.  

**Project Overview:**

ABC Supply seeks to understand customer behavior and product performance better. This project will delve into their data to answer key questions like:

* **How do different notification types affect product usage?**
* **Which products receive the most support requests?**
* **Are there patterns in product usage based on customer demographics?**
* **Is there other data that would be valuable and what data management we should be doing to obtain it?**

By analyzing these trends, we aim to provide ABC Supply with valuable information to optimize their product offerings and customer engagement strategies.

<img width="893" alt="image" src="https://github.com/user-attachments/assets/6850c8d1-648f-4781-beda-56a95e18ccbd" />


**Technical Approach:**

1. **Data Acquisition and Processing:** We will employ Python libraries like Polars for efficient data transformation and manipulation, ensuring a robust data pipeline.
2. **Stakeholder Interviews:**  We will conduct interviews with key stakeholders at ABC Supply to gather requirements, understand business context, and refine our analytical objectives.
3. **Business Process Diagramming:**  Taking the interviews with stakeholders, create visuals that depict the process that generates the data provided in the project.
4. **Exploratory Data Analysis (EDA):** We will utilize Python libraries like Pandas and Scikit-learn to perform comprehensive EDA, identifying patterns, correlations, and outliers within the data.
5. **Data Modeling:** Consuming the information gained, take the raw data and build a data model that supports answering the questions or providing new insights.  Share that model with diagrams like ERD and Data Dictionaries.
6. **Data Visualization:** Streamlit will be used to develop an interactive web application that visually presents our findings in a clear and intuitive manner. 

**Development Workflow:**

We adhere to a strict feature branching workflow for version control using Git:

* **`main` Branch:**  This branch represents the stable, production-ready codebase.
* **`development` Branch:**  This branch serves as the primary development hub for new features and bug fixes.

https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow

Pull requests will be submitted from the `development` branch to the `main` branch for review and merging after successful testing.  At the end of each sprint the team should have their demo materials/solutions in the main branch.

**Deliverables:**

* A functional Streamlit web application showcasing our findings and interactive data visualizations.
    * This application should be stored in the folder "app".
    * The application should include any final dashboards, visuals and data management interfaces needed.
    * The application should follow the directory structure stubbed in the repo.
    * Plan to use a multi-page app to allow contributors to work on different pages in the application at one time.
    * https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
    * No raw data should be used in the application.  All data should be optimized and remodeled and stored in the "/app/datasets/" folder.
* Data pipelines written as jupyter notebooks.
    * Please use polars as the dataframe library.
    * Those notebooks should be stored in the pipelines directory.
    * One notebook per transformation output.
    * Each notebook should have all imports in the first cell.
    * All data inputs in the next set of cells.
    * Transformations in the middle
    * Last cell should contain the write to the transformed data folder.
* All EDA notebooks, scripts, outputs, presentations can be saved in the EDA folder.
* All datasets should be stored in the data root folder.
    * All raw data provided for the project will be in the "raw" folder.  These files should never change or be overwritten by the project team.
    * Any changes to the raw data should be handled through the data pipeline notebooks.
    * Any changes should be saved in "transformed" folder.  No updates to raw files ever.
    * For the final application a copy of the final data model(s) can be saved in the "/app/datasets/" folder.
    * All data artifacts like data dictionaries and ERDs should be stored in the "/data/artifacts/" folder.
    * A stub data dictionary in markdown will be available for copying and use.  All datasets including the raw datasets are required to have a data dictionary completed.
* A comprehensive powerpoint report documenting our methodology, key insights, and recommendations for ABC Supply.

**Source Data:**

In most real analytical product builds there is data sourcing required.  As the students will not be operating as employees, all source data is provided already. This data does not have any ABC associate information in it.  And has been anonymozied.

This data is located in the "\Data\Raw\" folder of the repo.

|Source | Description | File Name |
|-------|-------------|-----------|
|Oracle Analytics Cloud | Logs of analytical actions in the platform. | answers_log.csv |
|Active Directory | Export of associate details from the work directory. | associate_export.parquet |
|Analytics Hub| Collection export of notifications documents. | hub_notifications.json |
|Analytics Hub| Collection export of notification view logs. | hub_notification_logs.json |
|Analytics Hub| Collection export of quick guide log documents. | hub_quick_guide_logs.json |
|Analytics Hub| Collection export of users documents. | hub_users.json |
|Analytics Hub| Collection export of roles documents. | roles.json |
|Analytics Hub| Collection export of tile user metrics documents. | tile_user_metrics.json |
|Analytics Hub| Collection export of tile documents. | tiles.json |
|Tableau | Logs of views in Tableau. | tableau_logs.csv |
|Service Now | Incidents submitted to our support teams. | incidents.csv |

**Tools and Technologies:**  (All tools work on Windows/Linux/ Mac (Intel or ARM))

* Python 3.x
    * Versatility: Python is a general-purpose programming language that can be used across various domains, including web development, automation, data analysis, machine learning, and more.
    * Rich Ecosystem: It boasts an extensive ecosystem of libraries for data manipulation (Pandas), numerical computing (NumPy), machine learning (Scikit-learn), and web applications (Streamlit).
    * Ease of Learning: Its syntax is clear and intuitive, making it accessible to beginners while still being powerful enough for experts.
* Polars  (Pandas as needed)   https://pola.rs
    * Performance Efficiency: Polars utilizes Apache Arrow under the hood to provide high-speed computation on large datasets compared to traditional relational databases or even Pandas.
    * Memory Management: Its lazy execution model optimizes memory usage by deferring computations until necessary.
    * Scalable Analytics: Ideal for processing big data due to its design principles rooted in performance optimization.
* DuckDB  (If the team wants a database to store and interact with the data in structured query language.)   https://duckdb.org
  * Lightweight and Embedded: Unlike traditional databases requiring extensive configuration or server setups, DuckDB can be embedded directly into applications or run as an in-memory engine without setup overhead.
  * Can be saved as a file and shared with others.
* Scikit-learn or other Statistical Analysis Libraries
* Streamlit  https://streamlit.io
* Git   https://git-scm.com
* Tableau Desktop https://www.tableau.com/academic/students
* Visual Studio Code  https://code.visualstudio.com
* Miro (link to be provided).  Planning\Grooming\Diagramming

**The project utilizes anonymized internal data from ABC Supply. All team members must adhere to relevant privacy regulations regarding this data.  All data should be processed locally on student's computers.  Data should not be uploaded to any service or shared file system other than this git repository. Any dissemination or use outside of this project scope requires explicit authorization from ABC Supply.**
