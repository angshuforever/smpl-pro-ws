# Personal Expense Tracker

## Overview
A Python application for managing personal expenses with budget tracking capabilities. Users can add, view, and analyze expenses while monitoring their monthly budget.

## Features

### 1. Expense Management
- Add expenses with date, category, amount, and description
- View all expenses with category-wise totals
- Data validation for dates and amounts
- Predefined expense categories:
  - Food
  - Transportation
  - Housing
  - Entertainment
  - Utilities
  - Other

### 2. Budget Features
- Set monthly budget
- Track expenses against budget
- Warning alerts for:
  - Budget exceeded
  - Near budget limit (80% used)

### 3. Data Persistence
- Auto-saves expenses to CSV file
- Loads previous expenses on startup
- Safe exit with data saving

## Technical Requirements
- Python 3.x
- Dependencies:
  - pandas
  - datetime
  - IPython

## Data Structure
```python
{
    'date': 'YYYY-MM-DD',
    'category': 'Category Name',
    'amount': float,
    'description': 'string'
}
```

## Validation Rules
- Date: Must be in YYYY-MM-DD format
- Amount: Must be positive number
- Category: Must be from predefined list
- Description: Cannot be empty

## File Structure
- expenses.csv: Stores expense records
- Main class: ExpenseTracker
- Interactive menu-driven interface
