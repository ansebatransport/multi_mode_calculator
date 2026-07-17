"""Web Calculator - Flask backend."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from flask import Flask, render_template, request, jsonify
from core.engine import ExpressionEvaluator
from core.expression_parser import ShuntingYardParser
from core.base_converter import BaseConverter
from core.financial import FinancialCalculator
from core.unit_converter import UnitConverter
from core.worksheets import WorksheetCalculator

app = Flask(__name__)
engine = ExpressionEvaluator()
parser = ShuntingYardParser()
unit_converter = UnitConverter()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({'error': 'No expression provided'}), 400
    try:
        engine.angle_mode = data.get('angle_mode', 'radians')
        tokens = parser.parse(data['expression'])
        result = engine.evaluate(tokens)
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/programmer/convert', methods=['POST'])
def programmer_convert():
    data = request.get_json()
    try:
        decimal_val = BaseConverter.to_decimal(data['value'], data['from_base'])
        result = BaseConverter.from_decimal(decimal_val, data['to_base'])
        all_bases = BaseConverter.to_all_bases(decimal_val)
        return jsonify({'result': result, 'decimal': decimal_val,
                        'hex': '0x' + all_bases['hex'], 'oct': '0o' + all_bases['oct'],
                        'bin': '0b' + all_bases['bin']})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/programmer/bitwise', methods=['POST'])
def programmer_bitwise():
    data = request.get_json()
    try:
        a, b = int(data['a']), int(data.get('b', 0))
        ops = {'AND': lambda: a & b, 'OR': lambda: a | b, 'XOR': lambda: a ^ b,
               'NOT': lambda: ~a, 'LSHIFT': lambda: a << b, 'RSHIFT': lambda: a >> b}
        result = ops[data['operator']]()
        all_bases = BaseConverter.to_all_bases(result)
        return jsonify({'result': result, 'decimal': result,
                        'hex': '0x' + all_bases['hex'], 'oct': '0o' + all_bases['oct'],
                        'bin': '0b' + all_bases['bin']})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/unit/categories', methods=['GET'])
def unit_categories():
    cats = unit_converter.get_categories()
    return jsonify({cat: [{'name': u.name, 'symbol': u.symbol}
                          for u in unit_converter.get_units(cat)] for cat in cats})


@app.route('/api/unit/convert', methods=['POST'])
def unit_convert():
    data = request.get_json()
    try:
        result = unit_converter.convert(float(data['value']),
                                        data['from_unit'], data['to_unit'], data['category'])
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/tvm', methods=['POST'])
def financial_tvm():
    data = request.get_json()
    try:
        return jsonify(FinancialCalculator.solve_tvm(
            n=data.get('n'), i_y=data.get('i_y'), pv=data.get('pv'),
            pmt=data.get('pmt'), fv=data.get('fv'),
            py=data.get('py', 12), cy=data.get('cy', 12), mode=data.get('mode', 'END')))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/npv', methods=['POST'])
def financial_npv():
    data = request.get_json()
    try:
        return jsonify({'result': FinancialCalculator.npv(data['rate'], data['cashflows'])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/irr', methods=['POST'])
def financial_irr():
    data = request.get_json()
    try:
        return jsonify({'result': FinancialCalculator.irr(data['cashflows'])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/mortgage', methods=['POST'])
def financial_mortgage():
    data = request.get_json()
    try:
        return jsonify(WorksheetCalculator.mortgage_monthly_payment(
            data['principal'], data['annual_rate'], data['years']))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/amortization', methods=['POST'])
def financial_amortization():
    data = request.get_json()
    try:
        schedule = FinancialCalculator.amortization_schedule(
            data['principal'], data['annual_rate'], data['months'])
        return jsonify({'schedule': schedule})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/depreciation', methods=['POST'])
def financial_depreciation():
    data = request.get_json()
    try:
        method = data.get('method', 'straight_line')
        cost, salvage, life = data['cost'], data['salvage'], data['life']
        if method == 'straight_line':
            schedule = FinancialCalculator.straight_line(cost, salvage, life)
        elif method == 'declining_balance':
            rate = data.get('rate')
            schedule = FinancialCalculator.declining_balance(cost, salvage, life, rate)
        elif method == 'sum_of_years':
            schedule = FinancialCalculator.sum_of_years(cost, salvage, life)
        else:
            return jsonify({'error': f'Unknown method: {method}'}), 400
        return jsonify({'schedule': schedule})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/bond', methods=['POST'])
def financial_bond():
    data = request.get_json()
    try:
        result = FinancialCalculator.bond_price(
            data['face'], data['coupon_rate'], data['ytm'], data['years'],
            data.get('freq', 2))
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/break_even', methods=['POST'])
def financial_break_even():
    data = request.get_json()
    try:
        return jsonify(FinancialCalculator.break_even(
            data['fixed_costs'], data['price_per_unit'], data['variable_cost_per_unit']))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/roi', methods=['POST'])
def financial_roi():
    data = request.get_json()
    try:
        return jsonify(FinancialCalculator.roi(
            data['investment'], data['return_value'], data.get('years', 1.0)))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/interest', methods=['POST'])
def financial_interest():
    data = request.get_json()
    try:
        mode = data.get('mode', 'compound')
        p, r, t = data['principal'], data['rate'], data['time']
        if mode == 'simple':
            result = WorksheetCalculator.simple_interest(p, r, t)
            return jsonify({'interest': result, 'total': round(p + result, 2)})
        else:
            n = data.get('periods', 12)
            amount = WorksheetCalculator.compound_interest(p, r, n, t)
            return jsonify({'amount': amount, 'interest': round(amount - p, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/car_loan', methods=['POST'])
def financial_car_loan():
    data = request.get_json()
    try:
        return jsonify(WorksheetCalculator.car_loan_payment(
            data['principal'], data['annual_rate'], data['months']))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/mirr', methods=['POST'])
def financial_mirr():
    data = request.get_json()
    try:
        result = FinancialCalculator.mirr(
            data['cashflows'], data['finance_rate'], data['reinvest_rate'])
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/financial/profit_margin', methods=['POST'])
def financial_profit_margin():
    data = request.get_json()
    try:
        return jsonify(FinancialCalculator.profit_margin(data['revenue'], data['cost']))
    except Exception as e:
        return jsonify({'error': str(e)}), 400
