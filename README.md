<table style=" width: 100%; border-collapse: collapse;">
  <tr>
    <td style="vertical-align: middle;">
      <img src="./Assets/logo_1.png" alt="CargoFul Logo" width="75">
    </td>
    <td style="vertical-align: middle; padding-left: 10px;">
      <h1 style="display: inline; font-size: 2em; font-weight: bold; margin: 0;">CargoFul Exercises</h1>
    </td>
  </tr>
</table>

Welcome to the **CargoFul Technical Interview Exercises** repository! This repository contains my solutions to analytical exercises completed as part of the technical interview process with CargoFul.

## Table of Contents
1. [Overview](#overview)
2. [Exercises](#exercises)
    - [Exercise 1: Time Series Analysis and Forecasting](#exercise-1-time-series-analysis-and-forecasting)
    - [Exercise 2: Spatial Analytics](#exercise-2-spatial-analytics)
    - [Exercise 3: SQL](#exercise-3-sql)
3. [Getting Started](#getting-started)
---

## Overview

This repository demonstrates my approaches to various data analysis and algorithm development challenges. Each exercise includes structured, self-contained code to allow for easy understanding and reproducibility of results.

> **⚠️ NOTE:** <span style="color: red;">Due to privacy concerns, the CSV file containing historical POS data is not included in this repository and is ignored during upload. Collaborators should manually upload the required CSV file in the `DATA` directory to run the code successfully.</span>

## Exercises

### Exercise 1: Time Series Analysis and Forecasting

This exercise involves analyzing and forecasting time series data for POS (points of sale) to predict future values for each location ID. The steps include data preprocessing, handling outliers, prioritizing specific POS IDs, and using a time series forecasting model.

#### Solution Outline:
1. **Dataset Quality Assessment**: Examine dataset structure, check for missing values, and review key patterns.
2. **POS IDs Prioritization**: Prioritize Point of Sale (POS) IDs based on forecast relevance.
3. **Outliers Cleaning**: Remove or adjust outliers to improve forecast accuracy.
4. **Cross-Validation**: Use cross-validation to evaluate model performance.
5. **Time Series Algorithm**: Apply a forecasting model to account for time-based trends and seasonality.
6. **Algorithm Assessment**: Evaluate model accuracy using metrics like RMSE or MAE.

You can view the Jupyter Notebook directly via [nbviewer](https://nbviewer.org/github/AtlasAnatomy/CargoFul_exercises/blob/main/Time_series_POS.ipynb).

### Exercise 2: Spatial Analytics

This exercise focuses on spatial data analysis, aimed at uncovering geographic patterns through clustering and distance calculations.

#### Solution Outline:
1. **Spatial Clustering**: Group data points based on geographic proximity.
2. **Distance Calculations**: Calculate distances between locations for spatial analysis.
3. **Visualization**: Generate maps to visualize spatial patterns.

### Exercise 3: SQL

The third exercise consists of SQL-based solutions for complex data retrieval and manipulation.

#### Solution Outline:
- **SQL Scripts**: Each query is optimized for efficient data extraction and manipulation. These SQL scripts are located in the `sql_queries/` directory, with a test function `test_sql_queries()` provided for performance validation.

## Getting Started

To view, test, and modify the solutions in this repository:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/CargoFul_exercises.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd CargoFul_exercises
    ```
3. **Create a Virtual Environment**:
    ```bash
    python -m venv venv   # For Windows
    venv\Scripts\activate
    ```
4. **Install dependencies** (e.g., time series and spatial libraries):
    ```bash
    pip install -r requirements.txt
    ```

---

Thank you for checking out my solutions and Happy coding!