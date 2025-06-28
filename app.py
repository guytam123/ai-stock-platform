
from flask import Flask, render_template, request, jsonify
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_stocks():
    symbol = request.form.get('symbol')
    data = yf.download(symbol, period='1mo', interval='1d')
    if data.empty:
        return jsonify({'error': 'לא נמצאו נתונים עבור הסימול המבוקש.'})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='מחיר סגירה'))
    graph_json = fig.to_json()
    return jsonify({'symbol': symbol.upper(), 'graph': graph_json})

if __name__ == '__main__':
    app.run(debug=True)
