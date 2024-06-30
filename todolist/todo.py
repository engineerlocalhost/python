def todo_list():
    tasks = []

    while True:
        print("\n1. Tambah Tugas")
        print("2. Tampilkan Tugas")
        print("3. Hapus Tugas")
        print("4. Keluar")

        choice = input("Pilih opsi: ")

        if choice == '1':
            task = input("Masukkan tugas: ")
            tasks.append(task)
            print("Tugas ditambahkan!")
        elif choice == '2':
            print("Daftar Tugas:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
        elif choice == '3':
            task_number = int(input("Masukkan nomor tugas yang akan dihapus: "))
            if 0 < task_number <= len(tasks):
                removed_task = tasks.pop(task_number - 1)
                print(f"Tugas '{removed_task}' dihapus!")
            else:
                print("Nomor tugas tidak valid.")
        elif choice == '4':
            break
        else:
            print("Pilihan tidak valid.")

todo_list()
