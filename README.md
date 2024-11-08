# ![CargoFul Logo](logo.png) CargoFul Exercises Codebase

Welcome to the **CargoFul Technical Interview Exercises** repository! This project contains code solutions to analytical exercises provided by CargoFul. Each solution is structured to be easily reviewed, tested, and improved for future use or enhancement.

## Table of Contents
1. [Overview](#overview)
2. [Exercises](#exercises)
    - [Exercise 1: Time Series Analysis and Forecasting](#exercise-1-time-series-analysis-and-forecasting)
    - [Exercise 2: Spatial Analytics](#exercise-2-spatial-analytics)
    - [Exercise 3: SQL](#exercise-3-sql)

---

## Overview

This repository demonstrates approaches to different types of data analysis and forecasting challenges. Each exercise has a clearly organized structure to facilitate code readability, testability, and easy modification for further experimentation or feature additions.

## Exercises

### Exercise 1: Time Series Analysis and Forecasting

This exercise focuses on analyzing and forecasting time series data, which is often used to project future values based on historical trends.

#### Solution Outline:
1. **Dataset Assessment**: Inspect the dataset structure, check for missing values, and review key patterns.
2. **POS IDs Prioritization**: Prioritize Point of Sale (POS) IDs based on forecast relevance. You can adjust prioritization criteria in the script under `pos_prioritization()`.
3. **Outliers Cleaning**: Remove or adjust outliers to improve forecast accuracy. Parameters for outlier detection can be modified in the `clean_outliers()` function.
4. **Cross-Validation**: Use cross-validation for model evaluation on different data subsets. Modify folds or methods within `cross_validation()` for enhanced evaluation.
5. **Time Series Algorithm**: Apply a forecasting model that accounts for time-based trends and seasonality. Customize algorithm parameters or swap out the model in the `apply_forecasting_model()` function.
6. **Algorithm Assessment**: Assess model accuracy using metrics like RMSE or MAE, which are configurable in the `evaluate_model()` function.

### Exercise 2: Spatial Analytics

The goal of this exercise is to analyze spatial data, typically to understand geographic patterns or clusters. 

#### Solution Outline:
1. **Spatial Clustering**: Cluster data points based on geographic proximity. Modify clustering parameters in `spatial_clustering()`.
2. **Distance Calculations**: Calculate distances between locations for spatial analysis. Adjust distance metrics or thresholds in `calculate_distances()`.
3. **Visualization**: Generate maps to visualize spatial patterns. Customize map settings and styles in `visualize_spatial_patterns()`.

### Exercise 3: SQL

This exercise showcases SQL solutions for complex data retrieval and manipulation challenges. 

#### Solution Outline:
- **SQL Scripts**: Each query is designed for efficient data extraction and manipulation. Edit SQL scripts in the `sql_queries/` directory, and use `test_sql_queries()` to test the accuracy and performance of each query.

---

Happy coding, and feel free to experiment with the code!
