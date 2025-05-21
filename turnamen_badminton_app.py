
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Jadwal Turnamen Badminton")

st.markdown("Aplikasi ini membantu membuat jadwal pertandingan untuk turnamen badminton single elimination.")

# Input pengguna
jumlah_pemain = st.number_input("Jumlah Pemain (max 64)", min_value=2, max_value=64, step=2, value=64)
jumlah_lapangan = st.number_input("Jumlah Lapangan", min_value=1, max_value=10, value=2)
durasi_pertandingan = st.number_input("Durasi Pertandingan (menit)", value=30)
waktu_mulai = st.time_input("Waktu Mulai", value=datetime.strptime("08:00", "%H:%M").time())

if st.button("Buat Jadwal"):
    round_1 = [(f"Player {i+1}", f"Player {i+2}") for i in range(0, jumlah_pemain, 2)]
    waktu = datetime.combine(datetime.today(), waktu_mulai)
    lapangan = 1
    jadwal = []

    for i, match in enumerate(round_1):
        jadwal.append({
            "No": i + 1,
            "Waktu": waktu.strftime("%H:%M"),
            "Lapangan": f"Lapangan {lapangan}",
            "Pemain 1": match[0],
            "Pemain 2": match[1]
        })
        if lapangan < jumlah_lapangan:
            lapangan += 1
        else:
            lapangan = 1
            waktu += timedelta(minutes=durasi_pertandingan)

    df = pd.DataFrame(jadwal)
    st.success("Jadwal berhasil dibuat!")
    st.dataframe(df)

    # Unduh sebagai Excel
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Jadwal')
    st.download_button(
        label="📥 Download Jadwal Excel",
        data=output.getvalue(),
        file_name="jadwal_turnamen_badminton.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
