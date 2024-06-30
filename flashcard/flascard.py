def flashcard():
    kartu = {
        "Ibukota Indonesia": "Jakarta",
        "2 + 2": "4",
        "Warna bendera Indonesia": "Merah Putih"
    }
    
    for pertanyaan, jawaban in kartu.items():
        jawaban_pengguna = input(f"{pertanyaan}: ")
        if jawaban_pengguna.lower() == jawaban.lower():
            print("Benar!")
        else:
            print(f"Salah! Jawaban yang benar adalah: {jawaban}")

flashcard()
