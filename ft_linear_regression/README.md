# ft_linear_regression

A simple machine learning project that predicts the daily log time (in minutes) of **each student** based on the date using linear regression. One model (θ₀, θ₁) is trained per student (`login`), never on all students together.

---

## Part 1: Train Model & Predict Program

### What is Linear Regression?

Linear regression finds a straight line that best fits your data. It answers: **"How do two variables relate?"**

In this project:
- **Input (X)**: Date (converted to a number of days)
- **Output (Y)**: Log time in minutes

The model learns: `LogTime = θ₀ + θ₁ × Days`

Where:
- `θ₀` = the base log time (intercept)
- `θ₁` = how much the log time changes per day (slope)

### How It Works

The algorithm uses **gradient descent** to find the best parameters:

1. Start with random values for θ₀ and θ₁
2. Make predictions and calculate errors
3. Adjust θ₀ and θ₁ to reduce errors
4. Repeat until the model converges

**What are θ₀ and θ₁?**

In gradient descent, we're trying to find the best values for these two numbers:
- **θ₀** (theta zero): The starting point of our line (y-intercept). Think of it as "the base log time"
- **θ₁** (theta one): The slope of our line. Think of it as "how much the log time changes each day"

The algorithm slowly adjusts both values little by little to make the predictions better and better.

Before training, data is **normalized** (scaled between 0-1) to improve performance.

### Quick Start

#### 1. Installation of the venv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. Train the model

```bash
python3 src/training_model/main.py [path/to/log_time.csv]
```

The csv path is optional (default: `data.csv`). This trains one model per student (data is normalized per student) and saves all parameters to `output.csv` (`login,theta0,theta1`). A student needs at least two different dates, otherwise he is skipped.

#### 3. Make predictions

```bash
python3 src/predict_program/main.py
```

Enter the `login` of a student and a date (`YYYY-MM-DD`) and get the predicted log time of this student.

### File Structure

```
training_model/
  ├── main.py              # Loads data and trains model
  ├── load.py              # Loads CSV file
  └── linear_function.py   # Gradient descent algorithm

predict_program/
  ├── main.py              # Makes predictions
  └── get_value.py         # Reads trained parameters
```

---

## Part 2: Bonus Features

### GUI Application

An interactive interface with visualization and performance metrics.

```bash
source ./venv/bin/activate
python3 src/bonus/main_bonus.py
```

**Features**:
- Choose the **period** of the regression: `day`, `week` or `month`. The log time of each student is summed by period (week: Monday to Sunday, 10080 minutes max; month: calendar month) and the linear regression is done on these totals. Each period has its own models (`output_bonus_day.csv`, `output_bonus_week.csv`, `output_bonus_month.csv`), so you have to launch the training for each period you want to see
- Only complete weeks / months of the csv are used (the first and last ones are often cut). A period without any presence counts as 0 minutes, except before the first period of presence of the student. A student needs at least two periods
- Train the models of all students with one click
- Choose the student (login) in a list
- View data visualization (scatter plot over time + regression line)
- "Display all" also draws the pace lines (hours per week: PACE8 = 61h, PACE12 = 35h, PACE15 = 25h, PACE18 = 19h, PACE22 = 15h, PACE24 = 10h), converted for the selected period: per day = week / 7 (PACE8 = 8.71h), per month = week × 4 (PACE8 = 244h)
- Display performance metrics (RMSE, R²)
- Save and load trained models

### Key Concepts

| Term | Meaning |
|------|---------|
| **MSE** | Average squared error (lower is better) |
| **RMSE** | Square root of MSE (same units as the log time: minutes) |
| **R²** | How well the model fits (0-1, higher is better) |
| **Normalization** | Scaling data between 0 and 1 |
| **Gradient Descent** | Algorithm to find best parameters |

---

## Dataset Format

The csv needs a `login` column (a `user_id` column is also accepted and used as the student name), a `date` column and a `log_time_minutes` column (or a `log_time` column as `HH:MM:SS`, converted to minutes). Other columns are ignored. Rows with invalid values are dropped; the rows are grouped by `login`.

```csv
login,date,log_time,log_time_minutes
dvignaud,2026-11-05,01:17:59.337711,77.99
dvignaud,2026-11-03,04:36:00.147232,276.0
dvignaud,2026-10-30,05:30:51.205698,330.85
```

---

## References

- [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course/linear-regression)
- [Overfitting Explained](https://medium.com/@rakeshandugala/the-art-of-balance-tackling-overfitting-and-underfitting-in-linear-regression-models-bc1517b892c8)
- [Regression Metrics](https://medium.com/analytics-vidhya/regression-and-performance-metrics-accuracy-precision-rmse-and-what-not-223348cfcafe)
- [PySimpleGUI Documentation](https://docs.pysimplegui.com/)