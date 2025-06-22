import streamlit as st
import joblib

# ===== Konfigurasi Tampilan =====
st.set_page_config(page_title="Kuis Kegiatan 2", page_icon="🌷")

# Background kuning muda
theme_color = "#fff9c4"
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {theme_color};
    }}
    </style>
""", unsafe_allow_html=True)

# ===== Judul dan Deskripsi =====
st.title("🎮 Kuis Interaktif - Kegiatan 2")
st.caption("Topik: Peluang (Rtnomatematika - Permainan Cublak-Cublak Suweng")

# ===== Petunjuk =====
with st.expander("📌 Petunjuk Pengerjaan", expanded=True):
    st.markdown("""
    - Masukkan nama kamu terlebih dahulu.
    - Jawablah semua soal pilihan ganda yang disediakan.
    - Setelah selesai, klik tombol **Kirim Jawaban** untuk melihat hasil.
    """)

# ===== Memuat Soal dari Model =====
soal_pilgan = joblib.load("hasil_kuis2.pkl")

# ===== Input Nama Siswa =====
if "nama_dikunci" not in st.session_state:
    st.session_state.nama_dikunci = False

if not st.session_state.nama_dikunci:
    nama = st.text_input("Masukkan nama kamu:")
    if nama:
        if st.button("Mulai Kuis"):
            st.session_state.nama = nama
            st.session_state.nama_dikunci = True

# ===== Kuis Dimulai =====
else:
    st.success(f"Halo, {st.session_state.nama}! Silakan mengerjakan kuis di bawah ini. Semangat ya 🎯")

    jawaban_pengguna = []
    skor = 0

    for i, soal in enumerate(soal_pilgan):
        st.markdown(f"**{i+1}. {soal['soal']}**")
        pilihan = st.radio("Pilih jawaban kamu:", soal['opsi'], key=f"soal_{i}")
        jawaban_pengguna.append(pilihan.strip()[:1])

    if st.button("📨 Kirim Jawaban"):
        st.subheader("📊 Hasil Jawaban")
        benar = 0

        for i, jawaban in enumerate(jawaban_pengguna):
            kunci = soal_pilgan[i]['jawaban']
            if jawaban == kunci:
                st.success(f"Soal {i+1}: ✅ Benar (Jawaban: {kunci})")
                benar += 1
            else:
                st.error(f"Soal {i+1}: ❌ Salah. Jawaban yang benar adalah {kunci}")

        total_soal = len(soal_pilgan)
        nilai = int((benar / total_soal) * 100)

        # ===== Ringkasan Nilai Akhir =====
        st.markdown("---")
        st.subheader("🎓 Ringkasan Nilai Akhir")
        st.markdown(f"""
            <div style='background-color: #fffde7; padding: 20px; border-radius: 10px; border: 1px solid #f0e68c;'>
                <h4>Nama: <b>{st.session_state.nama}</b></h4>
                <h5>Jawaban Benar: <b>{benar} dari {total_soal} soal</b></h5>
                <h3 style='color:#d84315;'>🎉 Nilai Akhir: <b>{nilai}/100</b></h3>
            </div>
        """, unsafe_allow_html=True)
