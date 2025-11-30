Overview project

Project ini merupakan projek untuk melatih dan mengingat kembali penggunaan python. 
Dimana pada projek ini dilakukan proses ETL yaitu Extract, Transform, and Load. 
Melakukan pengiriman request get untuk mengambil quote dengan API. Melakukan Pytest pada ETL yang telah dibuat.

ETL Flow

Untuk proses ETL yang dilakukan adalah seperti berikut: 
Load CSV -> Check empty row -> check missing mandatory column. -> amount, currency, transaction id, date format validation -> clean whitespace -> change date format from dd/mm/yyyy to yyyy-mm-dd -> impute merchant category with most often category -> convert string to datetime.date -> change numeric column to float -> derive 3 feature

Bangking validation rule

validasi mengikuti aturan dibawah dimana jika tidak sesuai akan terdapa log pemberitahuan invalid
transaction_id wajib mengikuti pola: TXNxxxxxxx
Tanggal harus memiliki format YYYY-MM-DD dan DD/MM/YYYY
amount tidak boleh bernilai negatif, kosong, lebih besar dari 10.000.000 IDR (flag anomaly)
currency harus salah satu dari: IDR, USD, SGD Lainnya (misal RP, XXX) merupakan invalid
direction harus DEBIT atau CREDIT
account_type harus salah satu dari: SAVINGS, CURRENT, CREDIT_CARD, LOAN

Cara running ETL

1. Pastikan library pandas dan aiohttp sudah terinstall
2. current directory harus pada folder bangking_etl_assessment
3. Jalan kan command berikut di command prompt python3 etl/__init__.py

Cara running test

1. Pastikan library pandas dan aiohttp sudah terinstall
2. current directory harus pada folder bangking_etl_assessment
3. Jalan kan command berikut di command prompt pytest

Possible Improvement

Kodingan kurang rapih dan beberapa fungsi kurang fleksibel dalam penggunaan sehingga kurang cocok digunakan pada daset lain. kurangnya handler apabila terjadi error.
