# Amazon Sales Exploratory Data Analysis (EDA)

A Python-based exploratory data analysis project using an Amazon sales report dataset. The project examines data quality, order status, product categories, recorded order amounts, regional patterns, monthly trends, correlations, and potential outliers.

## Project Objectives

- Understand the dataset structure and data types.
- Identify missing values, duplicate rows, and data-quality issues.
- Explore order status and product-category distributions.
- Compare recorded order amounts across categories and shipping states.
- Examine cancellation patterns across fulfilment methods.
- Analyze monthly changes in recorded order amounts.
- Investigate relationships between quantity and amount.
- Identify potential outliers and decide how to handle them based on evidence.
- Communicate findings, limitations, and possible business recommendations.

## Dataset

- **File:** `Amazon Sale Report.csv`
- **Initial size:** 128,975 rows and 24 columns.
- **Fields include:** order identifiers, dates, order status, fulfilment, sales channel, product category, quantity, amount, shipping information, and customer location fields.
- **Period:** the supplied records are primarily from March to June 2022.

Place the CSV in the `data/` directory. Add the original dataset source and its licence or usage terms here before publishing. Avoid publishing personal or sensitive data.

## Tools and Libraries

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Project Workflow

1. **Business understanding:** define the questions the analysis should answer.
2. **Data loading and inspection:** inspect the dataset shape, column names, data types, and summary statistics.
3. **Data quality assessment:** measure missing values, check duplicate rows, and validate important fields.
4. **Data cleaning:** standardize column names and data types and handle missing values only when justified.
5. **Univariate analysis:** examine individual variables such as order status, category, quantity, and amount.
6. **Bivariate and multivariate analysis:** compare variables to investigate relationships and differences.
7. **Time-based analysis:** explore monthly patterns while accounting for incomplete periods.
8. **Outlier investigation:** identify unusual values and inspect them before changing or removing data.
9. **Insights and recommendations:** document evidence-based findings and limitations.

## Business Questions

- Which order statuses appear most frequently?
- Which product categories have the highest row counts?
- Which categories have the highest summed recorded order amount?
- Which states have the highest summed recorded order amount?
- What share of rows is marked as cancelled?
- How does cancellation share differ by fulfilment method?
- How do recorded order amounts change by month?
- What data-quality issues could affect the results?
- Are there unusually high or low amounts that need investigation?
- How strongly are quantity and amount correlated in the analyzed rows?

## Initial Findings

The following are **preliminary findings** from the initial analysis. Recalculate them after applying final cleaning rules and verify the definitions used in each metric.

- The dataset contains 128,975 rows and 24 columns.
- The initial full-row duplicate check returned zero duplicate rows.
- `Set` and `kurta` have the largest category row counts in the initial category chart.
- `Set` has the highest summed recorded order amount in the initial category comparison.
- The initial analysis reports 18,332 rows marked `Cancelled`, approximately 14.2% of all rows.
- The initial cancellation crosstab reports 12.79% for Amazon fulfilment and 17.47% for Merchant fulfilment.
- Recorded order amount totals decline from April to June 2022 in the initial monthly aggregation. March has far fewer rows than the following months.
- The initial quantity-to-amount correlation is approximately 0.07.
- The IQR rule flags 3,600 amount observations as potential outliers.
- Missing values occur in multiple columns, including `fulfilled_by`, `promotion_ids`, `currency`, `amount`, and `courier_status`.

These are descriptive findings, not proof of causes. Summed `Amount` should be called **recorded order amount** unless the dataset's business definition and order-status rules support treating it as realized revenue.

## Recommended Project Structure

```text
Amazon-Sales-EDA/
├── data/
│   └── Amazon Sale Report.csv
├── notebooks/
│   └── amazon_sales_eda.ipynb
├── outputs/
│   ├── charts/
│   └── insights.txt
└── README.md
```

Update the filenames if your actual project structure differs.

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Amazon-Sales-EDA
```

### 2. Install the required libraries

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### 3. Start Jupyter Notebook

```bash
jupyter notebook
```

Open `notebooks/amazon_sales_eda.ipynb` and run the cells in order.

### 4. Load the dataset

If the notebook is inside `notebooks/` and the CSV is inside `data/`, use:

```python
import pandas as pd

df = pd.read_csv("../data/Amazon Sale Report.csv", low_memory=False)

print("Dataset shape:", df.shape)
display(df.head())
df.info()
```

## Data Quality and Interpretation Notes

- A repeated order ID is not necessarily a duplicate row; one order may contain multiple item records.
- Do not automatically replace missing amounts with zero.
- Remove an entirely empty column only after confirming that it contains no useful information.
- Treat postal codes as identifiers, not measurements.
- Investigate missing dates and invalid date values before time-based analysis.
- Check order status before interpreting summed amounts as completed sales.
- Outliers are observations flagged by a rule, not automatically errors.
- Distinguish row counts from unique order counts in charts and explanations.
- Compare months carefully when the dataset contains incomplete or unusually small periods.

## Limitations

- The data is historical and may not represent current sales.
- The dataset does not provide enough cost information to calculate profit reliably.
- Available fields may not explain the reasons behind cancellations or delivery issues.
- The findings describe observed patterns and associations; they do not establish causation.
- Results may change after cleaning decisions and metric definitions are finalized.

## Conclusion

This project follows a structured EDA workflow: inspect the dataset, assess data quality, explore distributions and relationships, visualize patterns, and translate validated results into business questions and recommendations. The final conclusions should be updated after the complete notebook has been run and all reported figures have been verified.

## Author

**Ravi Kumar**  
**Project:** Amazon Sales Exploratory Data Analysis (EDA)
