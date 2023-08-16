#William Davis | August, 16, 2023

from flask import Flask, request, jsonify
from collections import defaultdict
import datetime
import logging

app = Flask(__name__)

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Sample data structures to simulate database
inventory = {}
sales_data = []
advertisements = []
operations_budget = {
    'sales': 0,
    'marketing': 0,
    'hr': 0,
    'procurement': 0
}

# Inventory management
@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        data = request.json
        item_name = data['item_name']
        quantity = data['quantity']
        inventory[item_name] = quantity
        return jsonify({'message': 'Item added successfully'})
    except Exception as e:
        logging.error(f"Error adding item: {str(e)}")
        return jsonify({'error': 'Invalid input'}), 400

@app.route('/get_inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

# Sales tracking
@app.route('/add_sale', methods=['POST'])
def add_sale():
    try:
        data = request.json
        sales_data.append(data)
        return jsonify({'message': 'Sale added successfully'})
    except Exception as e:
        logging.error(f"Error adding sale: {str(e)}")
        return jsonify({'error': 'Invalid input'}), 400

@app.route('/get_sales', methods=['GET'])
def get_sales():
    return jsonify(sales_data)

# Advertisement management
@app.route('/add_advertisement', methods=['POST'])
def add_advertisement():
    try:
        data = request.json
        advertisements.append(data)
        return jsonify({'message': 'Advertisement added successfully'})
    except Exception as e:
        logging.error(f"Error adding advertisement: {str(e)}")
        return jsonify({'error': 'Invalid input'}), 400

@app.route('/get_advertisements', methods=['GET'])
def get_advertisements():
    return jsonify(advertisements)

# Financial forecasting algorithm
def forecast_financials(sales_data, advertisement_costs):
    total_revenue = sum(sale['amount'] for sale in sales_data)
    total_costs = sum(ad['cost'] for ad in advertisement_costs)
    net_profit = total_revenue - total_costs
    return net_profit

# Sales analysis function
def analyze_sales(time_period=None):
    today = datetime.date.today()
    sales_by_period = defaultdict(list)
    for sale in sales_data:
        sale_date = datetime.datetime.strptime(sale['date'], '%Y-%m-%d').date()
        if time_period is None or (today - sale_date).days <= time_period:
            sales_by_period[sale_date.strftime('%Y-%m')].append(sale)

    metrics = {}
    metrics['total_orders'] = sum(len(sales) for sales in sales_by_period.values())
    metrics['average_order_value'] = sum(sale['amount'] for sales in sales_by_period.values()) / metrics['total_orders']
    metrics['average_items_per_order'] = sum(len(sale['items']) for sales in sales_by_period.values()) / metrics['total_orders']

    return metrics

# Overview section
@app.route('/get_overview', methods=['GET'])
def get_overview():
    total_items = len(inventory)
    total_sales = len(sales_data)
    total_advertisements = len(advertisements)
    inventory_level = sum(inventory.values())

    # Calculate pie chart data
    total_budget = sum(operations_budget.values())
    pie_chart_data = {category: (budget / total_budget) * 100 for category, budget in operations_budget.items()}

    # Calculate financial metrics
    burn_rate = calculate_burn_rate()
    cash_balance = calculate_cash_balance()
    gross_sales = calculate_gross_sales()
    gross_profit = calculate_gross_profit()
    cost_of_goods_sold = calculate_cost_of_goods_sold()
    gross_margin = calculate_gross_margin()

    # Calculate financial ratings
    financial_ratings = calculate_financial_ratings()

    # Calculate risk assessment
    risk_grade = calculate_risk(financial_ratings)

    overview_data = {
        'total_items': total_items,
        'total_sales': total_sales,
        'total_advertisements': total_advertisements,
        'inventory_level': inventory_level,
        'pie_chart_data': pie_chart_data,
        'burn_rate': burn_rate,
        'cash_balance': cash_balance,
        'gross_sales': gross_sales,
        'gross_profit': gross_profit,
        'cost_of_goods_sold': cost_of_goods_sold,
        'gross_margin': gross_margin,
        'financial_ratings': financial_ratings,
        'risk_grade': risk_grade
    }
    return jsonify(overview_data)

# Operations section
@app.route('/set_operations_budget', methods=['POST'])
def set_operations_budget():
    try:
        data = request.json
        for category, budget in data.items():
            operations_budget[category] = budget
        return jsonify({'message': 'Operations budget set successfully'})
    except Exception as e:
        logging.error(f"Error setting operations budget: {str(e)}")
        return jsonify({'error': 'Invalid input'}), 400

@app.route('/get_operations_budget', methods=['GET'])
def get_operations_budget():
    return jsonify(operations_budget)

# Pie chart algorithm
def calculate_pie_chart():
    total_budget = sum(operations_budget.values())
    percentages = {category: (budget / total_budget) * 100 for category, budget in operations_budget.items()}
    return percentages

@app.route('/pie_chart', methods=['GET'])
def get_pie_chart():
    pie_chart_data = calculate_pie_chart()
    return jsonify(pie_chart_data)

# Financials section

# Calculate Burn Rate
def calculate_burn_rate():
    total_expenses = sum(operations_budget.values())
    days_in_month = 30  # Assume 30 days in a month
    burn_rate = total_expenses / days_in_month
    return burn_rate

# Calculate Cash Balance
def calculate_cash_balance():
    initial_cash = 100000  # Placeholder initial cash amount
    total_revenue = sum(sale['amount'] for sale in sales_data)
    total_expenses = sum(ad['cost'] for ad in advertisements) + sum(operations_budget.values())
    cash_balance = initial_cash + total_revenue - total_expenses
    return cash_balance

# Calculate Gross Sales
def calculate_gross_sales():
    total_revenue = sum(sale['amount'] for sale in sales_data)
    return total_revenue

# Calculate Gross Profit
def calculate_gross_profit():
    total_revenue = sum(sale['amount'] for sale in sales_data)
    total_costs = sum(ad['cost'] for ad in advertisements) + calculate_cost_of_goods_sold()
    gross_profit = total_revenue - total_costs
    return gross_profit

# Calculate Cost of Goods Sold
def calculate_cost_of_goods_sold():
    total_items_sold = sum(len(sale['items']) for sale in sales_data)
    cost_per_item = 10  # Placeholder cost per item
    cost_of_goods_sold = total_items_sold * cost_per_item
    return cost_of_goods_sold

# Calculate Gross Margin
def calculate_gross_margin():
    gross_profit = calculate_gross_profit()
    total_revenue = sum(sale['amount'] for sale in sales_data)
    gross_margin = (gross_profit / total_revenue) * 100
    return gross_margin

# Calculate Financial Ratings
# The next four functions are a very simple algorithm that return a letter grade based off data to calculate risk.
# This is an extremely simple concept, and i'm sure isn't applicable in real practice.
# This should be **COMPLETELY** replaced by AI or a complex algorithm, this is just filler code; and should **NOT** be used in even a beta version.
def calculate_financial_ratings():
    burn_rate = calculate_burn_rate()
    cash_balance = calculate_cash_balance()
    gross_margin = calculate_gross_margin()

    # Assign ratings based on thresholds
    ratings = {
        'burn_rate': 'A' if burn_rate <= 5000 else 'B' if burn_rate <= 10000 else 'C' if burn_rate <= 15000 else 'D',
        'cash_balance': 'A' if cash_balance > 0 else 'B' if cash_balance >= -10000 else 'C' if cash_balance >= -20000 else 'D',
        'gross_margin': 'A' if gross_margin >= 50 else 'B' if gross_margin >= 40 else 'C' if gross_margin >= 30 else 'D'
    }
    return ratings

# Calculate Overall Risk Letter Grade
def calculate_risk(financial_ratings):
    risk_factors = {
        'burn_rate': financial_ratings['burn_rate'],
        'cash_balance': financial_ratings['cash_balance'],
        'gross_margin': financial_ratings['gross_margin']
    }

    weighted_scores = {
        'burn_rate': 0.4,
        'cash_balance': 0.3,
        'gross_margin': 0.3
    }

    total_weighted_score = sum(weighted_scores[factor] * calculate_factor_score(risk_factors[factor]) for factor in risk_factors)

    risk_grade = calculate_grade(total_weighted_score)
    return risk_grade

# Calculate Factor Score
def calculate_factor_score(rating):
    if rating == 'A':
        return 5
    elif rating == 'B':
        return 4
    elif rating == 'C':
        return 3
    elif rating == 'D':
        return 2
    else:  # 'F' or 'F-'
        return 1

# Calculate Final Grade
def calculate_grade(total_score):
    if total_score >= 4.5:
        return 'A'
    elif total_score >= 3.5:
        return 'B'
    elif total_score >= 2.5:
        return 'C'
    elif total_score >= 1.5:
        return 'D'
    else:
        return 'F-'

if __name__ == '__main__':
    app.run(debug=True)
