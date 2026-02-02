import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("saldo.json")

saldo = 0.0
transactions = []

def load_data():
    global saldo, transactions
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                saldo = float(data.get("saldo", 0))
                transactions = data.get("transactions", []) or []
        else:
            saldo = 0.0
            transactions = []
    except (ValueError, json.JSONDecodeError):
        print("Peringatan: file saldo.json rusak. Mengatur saldo ke 0.")
        saldo = 0.0
        transactions = []

def save_data():
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump({"saldo": saldo, "transactions": transactions}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Gagal menyimpan data: {e}")

# muat data saat program mulai
load_data()

def tambah_pemasukan():
    global saldo
    try:
        jumlah = float(input("Masukkan jumlah pemasukan: "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0")
            return
    except ValueError:
        print("Input tidak valid")
        return
    saldo += jumlah
    transactions.append({"type": "pemasukan", "amount": jumlah, "timestamp": datetime.now().isoformat()})
    save_data()
    print(f"Berhasil menambahkan pemasukan sebesar {jumlah:.2f}. Saldo sekarang: {saldo:.2f}")

def tambah_pengeluaran():
    global saldo
    try:
        jumlah = float(input("Masukkan jumlah pengeluaran: "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0")
            return
    except ValueError:
        print("Input tidak valid")
        return
    if jumlah > saldo:
        print("Saldo tidak cukup")
        return
    saldo -= jumlah
    transactions.append({"type": "pengeluaran", "amount": jumlah, "timestamp": datetime.now().isoformat()})
    save_data()
    print(f"Berhasil melakukan pengeluaran sebesar {jumlah:.2f}. Saldo sekarang: {saldo:.2f}")

def lihat_saldo():
    global saldo
    print("=== Saldo Saat Ini ===")
    print(f"Rp {saldo:,.2f}")

def laporan():
    global saldo, transactions
    if not transactions:
        print("Belum ada transaksi.")
        return
    total_pemasukan = sum(t["amount"] for t in transactions if t["type"] == "pemasukan")
    total_pengeluaran = sum(t["amount"] for t in transactions if t["type"] == "pengeluaran")
    print("=== Laporan Transaksi ===")
    print(f"Total pemasukan : Rp {total_pemasukan:,.2f}")
    print(f"Total pengeluaran: Rp {total_pengeluaran:,.2f}")
    print(f"Saldo saat ini   : Rp {saldo:,.2f}")
    print("\nRiwayat transaksi (10 terakhir):")
    for t in transactions[-10:]:
        ts = t.get("timestamp", "")
        typ = "Masuk" if t["type"] == "pemasukan" else "Keluar"
        print(f"- {ts} | {typ} | Rp {t['amount']:,.2f}")

def menu():
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah pemasukan")
    print("2. Tambah pengeluaran")
    print("3. Lihat saldo")
    print("4. Keluar")
    print("5. Laporan")

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "4":
        print("Terima kasih!")
        break
    elif pilihan == "5":
        laporan()
    else:
        print("Pilihan tidak valid")