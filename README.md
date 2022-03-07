# MiM_Analytics_Tesis
 
This repository was created for the Master in Management & Analytics Thesis.

The aim of this project is to develop a data-driven scouting tool was developed to search and evaluate football players in Latin America, reducing time and costs involved in the process. This was achieved by designing, developing and implementing all stages of the pipeline, from the extraction of the data and storage in a datawarehouse, to the statistical analysis and graphical representation in a user-friendly web application.


**Contents**

**data_etls**

This folder contains all necessary scripts for the EtLT process that retrieves the data from the API and stores it in the PostgreSQL database. The code files contain the classes described in section 3.2.2 ELT vs ETL vs EtLT.

**data_queries**

This folder contains all SQL queries used for creating the Analytical Base Table presented in section 3.3 Analytical Base Table and described in Appendix C.

**performance_index**

This folder contains a jupyter notebook used for developing the players’ performance index. Its sections include the preprocessing of the variables (P90, Possession-adjusted), normalization, factor analysis, validation, graphical representation and sensitivity analysis. This process is then modularized in the four scripts PI_Preprocessing, PI_FactorAnalysis, PI_Scoring and PI_Main, all described in section 3.4 Statistical Analysis.

**dash_app**

This folder contains the scripts for the two views of the web application (Scouting and Player) presented in section 4.2 Football Analytics Web Application. By running these scripts the user can interact with the data and search and evaluate players in the different leagues, seasons and teams. It also includes a script for preprocessing the data.

**datasets**

This folder contains the final Analytical Base Table exported into a CSV file. This dataset is used for feeding the web application.

**plots_and_tables**

This folder contains all the plots and tables presented throughout the present thesis. They were all generated in one of the different stages of the pipeline.

**sandbox**

This folder contains scripts and notebooks with practice code and different approaches that were tried during the elaboration of the present thesis.
