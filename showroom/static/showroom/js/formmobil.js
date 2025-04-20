const checkboxDanaBank = document.getElementById('toggleDanaBank');
const rowTglPinjaman = document.getElementById('rowTglPinjaman');
const inpTglPinjaman = document.getElementById('id_tgl_pinjaman');
const rowDanaPinjaman = document.getElementById('rowDanaPinjaman');
const inpDanaPinjaman = document.getElementById('id_dana_pinjaman');
const rowSukuBunga = document.getElementById('rowSukuBunga');
const inpSukuBunga = document.getElementById('id_suku_bunga');
const rowLamaPinjaman = document.getElementById('rowLamaPinjaman');
const inpLamaPinjaman = document.getElementById('id_lama_pinjaman');

function toggleDanaBank() {
    const show = checkboxDanaBank.checked;
    rowTglPinjaman.style.display = show ? '' :'none';
    rowDanaPinjaman.style.display = show ? '' :'none';
    rowSukuBunga.style.display = show ? '' :'none';
    rowLamaPinjaman.style.display = show ? '' :'none';
    
    inpTglPinjaman.required = show;
    inpDanaPinjaman.required = show;
    inpSukuBunga.required = show;
    inpLamaPinjaman.required = show;

    inpTglPinjaman.disabled = !show;
    inpDanaPinjaman.disabled = !show;
    inpSukuBunga.disabled = !show;
    inpLamaPinjaman.disabled = !show;
}

checkboxDanaBank.addEventListener('change', toggleDanaBank);
window.addEventListener('DOMContentLoaded', toggleDanaBank);