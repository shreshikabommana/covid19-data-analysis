# Mapping Mortality: A Statistical Insight into COVID-19 Spread and Impact

This project presents a comprehensive visual and interactive analysis of the COVID-19 pandemic in the United States, focusing on trends in confirmed cases and deaths. Using publicly available datasets, the study explores key patterns in the trajectory of the virus from early January to late August 2020. The project uses various statistical methods, including moving averages and trend analysis, to reveal insights into the spread, mortality, and regional disparities of COVID-19.

## Table of Contents
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Dataset Description](#dataset-description)
- [Methodology](#methodology)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Interactive Dash Visualizations](#interactive-dash-visualizations)
- [Contributions and Findings](#contributions-and-findings)
- [Future Work](#future-work)

## Abstract

This study provides an interactive and visual analysis of COVID-19 trends in the United States, focusing on confirmed cases and deaths. The analysis is based on publicly available datasets and spans from January 2020 to August 2020. Key findings include an exploration of the temporal behavior of the death-to-case ratio, a comparison of case and death growth, and the identification of regional disparities. The project also includes interactive dashboards for dynamic exploration of the data.

## Introduction

The COVID-19 pandemic emerged in late 2019 and rapidly became a global health crisis. This study uses statistical analysis and data visualization techniques to understand the progression of COVID-19 in the U.S. By leveraging both static and dynamic visualizations, the study aims to provide insights into the severity, spread, and impact of the virus across the country. It also highlights how the pandemic evolved over time, with a particular focus on mortality trends and the effect of regional differences.

## Dataset Description

The datasets used in this study are sourced from Kaggle, specifically the "COVID-19 Analysis and Visualization" repository by Subhojit Paul. The data includes:

- **covid.csv**: Daily cumulative counts of confirmed COVID-19 cases and deaths by U.S. state, spanning from January 22, 2020, to July 27, 2020.
- **us_deaths_covid.csv**: Weekly aggregation of COVID-19 deaths by U.S. state, covering February 1, 2020, to August 29, 2020.

These datasets were preprocessed and cleaned for analysis, and rolling time-series aggregation was performed to generate trends and insights.

## Contents

- `data/` – Raw datasets (Excel)
- `output/` – Graphs and visualizations
- `notebook.ipynb` – Main analysis in Jupyter
- `report.pdf` – Final written report

## Methodology

The analysis includes several key steps:

1. **Preprocessing**: The datasets were cleaned using Python libraries such as pandas, numpy, and datetime. Missing values were addressed, and dates were converted to proper datetime formats.
2. **Exploratory Data Analysis (EDA)**: Visualizations were created using matplotlib and seaborn to explore the progression of cases and deaths over time. Key metrics such as the 7-day moving average were computed to smooth data and highlight trends.
3. **Ratio of Deaths to Cases**: A moving average ratio of new deaths to new cases was calculated to explore changes in the severity of the disease and the effectiveness of public health measures.
4. **Interactive Visualizations**: Dashboards were built using Plotly and Dash to enable interactive exploration of the data, including state-specific trends, age group analyses, and comorbidities.

## Interactive Dash Visualizations

### Mortality by Comorbidity and Age Range

This dashboard allows users to explore COVID-19 death counts by age group and underlying medical condition. The visualizations highlight how mortality varies by state for specific conditions like obesity, heart disease, and diabetes. The dashboard also reveals how the risk of mortality increases with age and pre-existing health conditions.

- [Link to Dashboard](http://127.0.0.1:8050/) (for local testing)

### Dynamic Time Series Dashboard

This dashboard provides a dynamic choropleth map of U.S. states, showing COVID-19 death counts aggregated by age group. Users can interactively filter by different age ranges to explore how mortality was distributed across the U.S. during the early stages of the pandemic.

- [Link to Dashboard](http://127.0.0.1:8051/) (for local testing)


## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/mapping-mortality.git
