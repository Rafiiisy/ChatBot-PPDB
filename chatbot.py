from utils.loader import load_jurusan, load_jadwal, load_video_poster

def handle_input(user_input):
    user_input = user_input.lower()

    if "profil" in user_input:
        data = load_video_poster()
        return f"🎥 {data['data_video_profil']['judul']}\n🔗 {data['data_video_profil']['link']}"

    elif "poster" in user_input:
        data = load_video_poster()
        return f"🖼️ {data['data_poster']['deskripsi']}\n🔗 {data['data_poster']['link']}"

    elif "jadwal" in user_input:
        jadwal = load_jadwal()
        response = "\n".join([f"{item['tanggal']} - {item['kegiatan']}" for item in jadwal])
        return response

    elif "daya tampung" in user_input:
        jurusan_data = load_jurusan()
        jalur = "afirmasi" if "afirmasi" in user_input else "reguler"
        jurusan_found = None
        for item in jurusan_data:
            if item['jurusan'].lower() in user_input:
                jurusan_found = item
                break
        if jurusan_found:
            j = jurusan_found['jurusan']
            d = jurusan_found['jalur'][jalur]
            return (
                f"📊 Jurusan: {j}\n"
                f"📍 Jalur: {jalur.title()}\n"
                f"👥 Daya Tampung: {d['daya_tampung']}\n"
                f"📉 Nilai Terendah: {d['nilai_terendah']}\n"
                f"📈 Nilai Tertinggi: {d['nilai_tertinggi']}\n"
                f"📊 Rata-Rata: {d['rata_rata']}"
            )
        else:
            return "Jurusan tidak ditemukan. Contoh: daya tampung kuliner afirmasi"

    else:
        return "Perintah tidak dikenali. Coba ketik: jadwal, daya tampung kuliner afirmasi, profil, atau poster."

# CLI loop
if __name__ == "__main__":
    print("🤖 Chatbot PMB SMKN 6 Yogyakarta Siap!")
    while True:
        user_input = input("👤 Kamu: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Sampai jumpa!")
            break
        print("🤖 Bot:", handle_input(user_input), "\n")
