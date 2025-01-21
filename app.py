import os
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
from flask import Flask, render_template, request
from math import comb
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# Folder untuk menyimpan gambar plot
PLOT_FOLDER = 'static/plots'
os.makedirs(PLOT_FOLDER, exist_ok=True)

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

def plot_pmf_cdf(n, p):
    """Membuat plot PMF dan CDF untuk distribusi binomial"""
    x = np.arange(0, n + 1)
    pmf = [binomial_probability(n, p, k)[0] for k in x]
    cdf = np.cumsum(pmf)  # Menghitung CDF manual

    # Plot PMF
    plt.figure(figsize=(10, 5))
    plt.bar(x, pmf, color='skyblue', alpha=0.7, label='PMF')
    plt.xlabel('k (Jumlah Keberhasilan)')
    plt.ylabel('Probabilitas')
    plt.title('Fungsi Massa Probabilitas (PMF)')
    plt.legend()
    pmf_path = os.path.join(PLOT_FOLDER, 'pmf.png')
    plt.savefig(pmf_path)
    plt.close()

    # Plot CDF
    plt.figure(figsize=(10, 5))
    plt.step(x, cdf, where='post', color='orange', label='CDF')
    plt.xlabel('k (Jumlah Keberhasilan)')
    plt.ylabel('Probabilitas Kumulatif')
    plt.title('Fungsi Distribusi Kumulatif (CDF)')
    plt.legend()
    cdf_path = os.path.join(PLOT_FOLDER, 'cdf.png')
    plt.savefig(cdf_path)
    plt.close()

    return pmf_path, cdf_path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Mendapatkan input dari form
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])

        # Validasi input
        if not (0 <= p <= 1):
            return render_template('index.html', error="Probabilitas p harus berada dalam rentang 0 hingga 1.")
        if not (0 <= k <= n):
            return render_template('index.html', error="Jumlah keberhasilan k harus berada dalam rentang 0 hingga n.")
        if n <= 0:
            return render_template('index.html', error="Jumlah percobaan n harus lebih besar dari 0.")

        # Menghitung probabilitas dan langkah perhitungan
        probability, steps = binomial_probability(n, p, k)
        # Membuat plot PMF dan CDF
        pmf_path, cdf_path = plot_pmf_cdf(n, p)

        # Menampilkan hasil pada template
        return render_template(
            'index.html',
            result=f'Probabilitas: {probability:.5f}',
            steps=steps,
            pmf_path=pmf_path,
            cdf_path=cdf_path
        )
    except ValueError:
        return render_template('index.html', error="Input tidak valid. Pastikan semua nilai diisi dengan benar.")

if __name__ == '__main__':
    app.run(debug=True)
