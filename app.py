import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Ambil credential dari secrets
creds_dict = st.secrets["google_service_account"]
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

client = gspread.authorize(creds)
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Mv08ZKODXyWbf75gMsb192OvTrVphy6mvoq_AypsPLA/edit")
worksheet = spreadsheet.worksheet("sheet1")  # atau nama sheet kamu

# ===================== DATA SOAL =====================
soal_pilgan = [
    {
        "soal": "1. Sari, Budi, Citra, Doni, dan Eka bermain Cublak-Cublak Suweng. Setelah hompimpa, Sari menjadi penebak dan duduk tengkurap di tengah, sedangkan 4 temannya duduk melingkar. Jika Sari menebak secara acak, berapakah peluang tebakannya benar?",
        "opsi": ["A. 1/4", "B. 1/5", "C. 1/3", "D. 1/2"],
        "jawaban": "B"
    },
    {
        "soal": "2. Ada sekelompok anak kecil terdiri dari 8 orang: Maya, Fajar, Lia, Riko, Arif, Bayu, Fito, dan Davin. Mereka hendak bermain “Cublak-cublak Suweng”. Untuk menentukan 1 orang yang tengkurap sebagai penebak batu/kecik, mereka melakukan hompimpa. Tentukan peluang kejadian bahwa Riko akan terpilih sebagai orang yang tengkurap!",
        "opsi": ["A. 2/8", "B. 0", "C. 1/8", "D. 1/6"],
        "jawaban": "C"
    },
    {
        "soal": "3. Dalam permainan Cublak-cublak Suweng yang dimainkan oleh 6 anak, 1 anak tengkurap menebak siapa yang menyembunyikan batu. Jika ia menebak salah, ia kalah. Tentukan peluang anak yang tengkurap kalah!",
        "opsi": ["A. 1/6", "B. 2/5", "C. 1/2", "D. 4/5"],
        "jawaban": "D"
    },
    {
        "soal": "4. Jika sebuah kotak berisi 6 bola merah, 2 bola biru, dan 4 bola hijau, berapakah peluang diambilnya bola biru atau hijau?",
        "opsi": ["A. 1/3", "B. 1/4", "C. 5/12", "D. 1/2"],
        "jawaban": "D"
    },
    {
        "soal": "5. Dalam sebuah undian terdapat 10 tiket, di mana 3 tiket adalah pemenang. Jika satu tiket diambil secara acak, berapakah peluang tiket yang diambil adalah tiket pemenang?",
        "opsi": ["A. 3/10", "B. 1/3", "C. 2/5", "D. 1/2"],
        "jawaban": "A"
    }
]

# ===================== TAMPILAN UTAMA =====================
st.set_page_config(page_title="Kuis Interaktif Kegiatan 2", page_icon="🎮")
st.title("🎮 Kuis Interaktif - Kegiatan 2")
st.image("https://cdn.pixabay.com/photo/2018/01/29/18/16/cube-3116778_640.jpg", use_container_width=True)
st.caption("Mengangkat nilai budaya dalam pembelajaran peluang 🎲 melalui permainan tradisional Cublak-Cublak Suweng.")

# ===================== INPUT NAMA SISWA =====================
nama = st.text_input("Masukkan nama kamu:")

if nama:
    with st.form("form_kuis"):
        st.subheader("📋 Soal Pilihan Ganda")
        jawaban_siswa = []
        for i, soal in enumerate(soal_pilgan):
            pilihan = st.radio(soal["soal"], soal["opsi"], key=f"soal_{i}")
            jawaban_siswa.append(pilihan)
        kirim = st.form_submit_button("✅ Kirim Jawaban")

    if kirim:
        benar = 0
        pembahasan = []

        for i, soal in enumerate(soal_pilgan):
            jawaban_user = jawaban_siswa[i][0]  # ambil huruf A/B/C/D
            kunci = soal["jawaban"]
            if jawaban_user == kunci:
                benar += 1
                pembahasan.append(f"✅ Soal {i+1}: Benar")
            else:
                pembahasan.append(f"❌ Soal {i+1}: Salah. Jawaban benar: {kunci}")

        nilai = int((benar / len(soal_pilgan)) * 100)

        # Animasi
        if nilai == 100:
            st.balloons()
        elif nilai >= 80:
            st.snow()

        # Hasil & Pembahasan
        st.success(f"🎉 {nama}, kamu menjawab benar {benar} dari {len(soal_pilgan)} soal.")
        st.info(f"📊 Nilai akhir kamu: {nilai}/100")

        with st.expander("🔍 Lihat Pembahasan"):
            for p in pembahasan:
                st.write(p)

        # ===================== SIMPAN KE GOOGLE SHEET =====================
        try:
            sheet.append_row([nama, nilai, benar, len(soal_pilgan), str(jawaban_siswa)])
            st.success("✅ Hasilmu berhasil disimpan ke Google Spreadsheet.")
        except Exception as e:
            st.error(f"Gagal menyimpan hasil: {e}")
