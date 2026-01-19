#Aplikasi game simpel number

secret_number = 67
guess_number = int(input("Masukkan angka tebakan: "))

while guess_number != secret_number:
    print("Jawaban salah.")
    print('Anda terjebak dalam loop.')
    guess_number = int(input("Masukkan angka lagi: "))

print('Tebakan anda benar. Selamat!')
print('Kode ini saya buat di codespace.')
