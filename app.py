import streamlit as st
import joblib

# === Konfigurasi halaman ===
st.set_page_config(page_title="🎲 Kuis Peluang - Kegiatan 2", page_icon="🎲")

# === Judul dan caption ===
st.title("🎲 Kuis Interaktif - Kegiatan 2")
st.caption("Topik: Peluang (Etnomatematika - Cublak-Cublak Suweng)")

# === Petunjuk pengerjaan ===
with st.expander("📌 Petunjuk Pengerjaan", expanded=True):
    st.markdown("""
    - Masukkan nama kamu terlebih dahulu.
    - Jawablah 5 soal pilihan ganda yang ditampilkan.
    - Klik **Kirim Jawaban** di bagian akhir untuk melihat hasil dan skor kamu.
    """)

# === Load soal dari model .pkl ===
soal_pilgan = joblib.load("hasil_kuis2.pkl")

# === Input nama siswa ===
if "nama_dikunci" not in st.session_state:
    st.session_state.nama_dikunci = False

if not st.session_state.nama_dikunci:
    nama = st.text_input("Masukkan nama kamu:")
    if nama:
        if st.button("Mulai Kuis"):
            st.session_state.nama = nama
            st.session_state.nama_dikunci = True

# === Jika nama sudah dikunci, tampilkan soal ===
else:
    st.success(f"Halo, {st.session_state.nama}! Yuk kita mulai kuisnya ✨")

    jawaban_pengguna = []
    for i, soal in enumerate(soal_pilgan):
        st.markdown(f"<b>{i+1}. {soal['soal'].replace(chr(10), '<br>')}</b>", unsafe_allow_html=True)
        jawaban = st.radio("Pilih jawaban kamu:", soal["opsi"], key=f"soal_{i}")
        jawaban_pengguna.append(jawaban.strip()[:1])  # Ambil huruf A/B/C/D

    # === Tombol submit jawaban ===
    if st.button("📨 Kirim Jawaban"):
        skor = 0
        benar = 0
        salah = 0
        st.subheader("📊 Hasil Jawaban")

        for i, jawaban in enumerate(jawaban_pengguna):
            kunci = soal_pilgan[i]["jawaban"]
            if jawaban == kunci:
                st.success(f"Soal {i+1}: ✅ Benar (Jawaban: {kunci})")
                skor += 1
                benar += 1
            else:
                st.error(f"Soal {i+1}: ❌ Salah. Jawaban yang benar: {kunci}")
                salah += 1

        total_soal = len(soal_pilgan)
        nilai = int((skor / total_soal) * 100)

        # === Ringkasan akhir ===
        st.markdown("---")
        st.subheader("🎓 Ringkasan Nilai Akhir")
        st.markdown(f"""
            <div style='
                background-color:#fffde7;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #f0e68c;
                font-size: 16px;
                line-height: 1.7;
            '>
                <b>Nama:</b> {st.session_state.nama}<br>
                <b>Jawaban Benar:</b> {benar} dari {total_soal} soal<br><br>
                <span style='font-size:22px; color:#d84315;'>🎉 <b>Nilai Akhir: {nilai}/100</b></span>
            </div>
        """, unsafe_allow_html=True)
