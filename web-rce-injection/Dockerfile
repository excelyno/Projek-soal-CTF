FROM python:3.11-slim

# Tambah user biasa agar pemain tidak punya akses root di dalam kontainer
RUN useradd -m ctf

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY ./app /app

# Taruh file Flag di lokasi rahasia dan set agar hanya bisa dibaca (Read-Only)
# Nama file sengaja dibuat acak sedikit agar pemain harus melakukan eksplorasi shell 'ls' dulu
RUN echo "CTF{r3m0t3_c0d3_3x3cut10n_j3b0l_w0k_2026}" > /home/ctf/flag_rahasia_992.txt

# Ubah kepemilikan folder ke user ctf
RUN chown -R ctf:ctf /app /home/ctf

# Tukar konteks eksekusi ke user biasa
USER ctf

EXPOSE 5000

CMD ["python", "app.py"]