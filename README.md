# Personal Finance Simulator

## Overview

Personal Finance Simulator is an innovative Python-based application designed to model and analyze personal financial scenarios. It offers a comprehensive suite of tools for managing and projecting personal finances, including cash flow management, asset and liability tracking, loan calculations, and complex event-based simulations. This project aims to provide users with a clear understanding of their financial health and assist in planning for future financial goals.

## Features

- **Cash Flow Management**: Track and manage monthly income and expenses.
- **Asset and Liability Tracking**: Monitor and calculate the value of assets and liabilities over time, providing a clear picture of net worth.
- **Loan Analysis**: Detailed loan management, including amortization schedules, interest calculations, and impact on overall finances.
- **Financial Event Simulation**: Simulate various life events (like purchasing a house, or changes in salary) and their impact on long-term financial health.
- **Data Visualization**: Graphical representation of financial data for easier understanding and analysis.
- **Customizable Scenarios**: Flexibility to create and test various financial scenarios based on user-defined parameters.

## Installation
1. Install Python
2. Set up a Python virtual environment and install necessary packages:
```
# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install packages from the requirements file
pip install -r requirements.txt
```
## Run the application
1. Edit/Add your financial hypothesis in the **src/variables.py** file.
#### Add Financial Entities (positive)
```python
# Define Financial Entity 

# Example Salary
salary = Entity(
    name="My Salary",               # Name of the entity
    amount=5000,                    # Monthly Amount of the entity
    annual_inflation_rate=4,        # Annual inflation rate of the entity
    start_date='2023-11-01'         # Start date of the entity
    end_date='2025-11-01'           # End date of the entity
    )
```
#### Add Financial Entities (negative)
```python
# Example Food
food = Entity(
    name="Food",                    # Name of the entity
    amount=-500,                    # Monthly Amount of the entity
    annual_inflation_rate=4,        # Annual inflation rate of the entity
    start_date='2023-11-01'         # Start date of the entity
    )
```
#### Add Financial Entities to the list of entities
```python
## Next, add entities to the list of entities
ENTITIES = [salary, food]           # List of entities to be simulated
```

#### Add Assets and Liabilities
```python
# Define Financial Entity (for example Salary)
loan= Loan(
    name="Home Loan",              # Name of the loan
    amount=800_000,                # Loan amount
    annual_interest_rate=6.5,      # Annual interest rate
    term_in_year=30,               # Term of the loan in years
    annual_inflation_rate=4,       # Annual inflation rate
    start_date='2023-11-01'        # Start date of the loan
    )
```
#### Add Assets and Liabilities to the list of assets and liabilities
```python
# next, add the loan to the list of assets and liabilities
ASSETS_LIAIBILITIES = [loan]        # List of assets and liabilities to be simulated
```
2. Run the simulation
```bash
python src/main.py
```