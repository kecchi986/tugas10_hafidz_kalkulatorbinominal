from flask import Flask, render_template, request
from math import comb

app = Flask(__name__)

def binomial_probability(n, p, k):
    """Menghitung probabilitas binomial dan langkah perhitungan"""
    coefficient = comb(n, k)
    success_prob = p ** k
    failure_prob = (1 - p) ** (n - k)
    probability = coefficient * success_prob * failure_prob
    steps = (
        f"Langkah perhitungan:\n"
        f"1. Koefisien Binomial: C({n}, {k}) = {coefficient}\n"
        f"2. Probabilitas Keberhasilan: {p}^{k} = {success_prob:.5f}\n"
        f"3. Probabilitas Kegagalan: (1 - {p})^{n - k} = {failure_prob:.5f}\n"
        f"4. Probabilitas Binomial: C({n}, {k}) * {p}^{k} * (1 - {p})^{n - k} = {probability:.5f}"
    )
    return probability, steps

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])

        if not (0 <= p <= 1):
            return render_template('index.html', error="Probabilitas p harus berada dalam rentang 0 hingga 1.")
        if not (0 <= k <= n):
            return render_template('index.html', error="Jumlah keberhasilan k harus berada dalam rentang 0 hingga n.")

        probability, steps = binomial_probability(n, p, k)
        return render_template('index.html', result=f'Probabilitas: {probability:.5f}', steps=steps)
    except ValueError:
        return render_template('index.html', error="Input tidak valid. Pastikan semua nilai diisi dengan benar.")

if __name__ == '__main__':
    app.run(debug=True)
