document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        const n = parseInt(document.getElementById("n").value);
        const p = parseFloat(document.getElementById("p").value);
        const k = parseInt(document.getElementById("k").value);

        if (isNaN(n) || isNaN(p) || isNaN(k) || p < 0 || p > 1 || k < 0 || k > n) {
            event.preventDefault();
            alert("Pastikan semua nilai diisi dengan benar dan sesuai batasan.");
        }
    });
});
