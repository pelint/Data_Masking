import sqlite3
import random
import sys

db_name='staff.db'
table="staff_info"

def connectDb():
	#Bu fonksiyon veritabanına bağlanmamızı sağlar.
	conn = sqlite3.connect(db_name)
	return conn

def createTable(table_name):
	#Bu fonksiyon tablo oluşturmamızı sağlar.
	conn=connectDb() #veri tabınına bağlanıldı.
	c=conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS "+table_name+"(staff_id INTEGER PRIMARY KEY AUTOINCREMENT ,TC VARCHAR(11) NOT NULL, salary VARCHAR NOT NULL, credit_card_number VARCHAR(19) NOT NULL )")
	conn.commit() #Veritabanı üzerindeki değişiklikler güncellendi.
	conn.close() #Veri tabanı bağlantısı kapatıldı.


def selectDbData(table_name):
	#Bu fonksiyon veritabanından veri okumamızı sağlar.
	conn=connectDb()
	c=conn.cursor()
	datas=c.execute("SELECT * FROM " + table_name)
	AllData=datas.fetchall() #tüm veriler liste olarak değişkene aktarıldı.
	return AllData

def CreateMaskedTC():
	#Bu fonksiyon TC maskelemek için kullanılır. Fonksiyon çağrıldığında bize 11 karakterlik random bir TC döndürür.
	MaskedTC=''
	for i in range(11):
		num=random.randint(0,9)
		MaskedTC=MaskedTC+str(num)
	return MaskedTC

def CreateMaskedSalary(salary):
	#Bu fonksiyon Ücreti maskelemek için kullanılır. Aldığı ücret parametresinin karakterlerinin kendi içerisinde yerlerini değiştirir.
	s=str(salary)
	MaskedSalary=''
	MaskedSalary=''.join(random.sample(s,len(s)))
	return MaskedSalary

def CreateMaskedCCNumber(CreditCardNumber):
	#Bu fonksiyon kredi kartı numarasını maskelemek için kullanılır. Parametre olarak aldığı kredi kartı numarasının ilk ve son dört 
	#hanesi dışındaki karakteleri gizler
	sizeOfCCN=len(CreditCardNumber)
	MaskedCreditCardNumber=''		
	MaskedCreditCardNumber=MaskedCreditCardNumber+CreditCardNumber[0:5]
	for i in range(5,sizeOfCCN-5):
		if CreditCardNumber[i]=='-':
			MaskedCreditCardNumber=MaskedCreditCardNumber+'-'
		else:
			MaskedCreditCardNumber=MaskedCreditCardNumber+"X"
	MaskedCreditCardNumber=MaskedCreditCardNumber+CreditCardNumber[sizeOfCCN-5:]
	return MaskedCreditCardNumber

	
def MaskAllTable():
	#Bu fonksiyon bir tablonun tamamı maskelenmek istediğinde kullanılır.
	StaffInfoList=selectDbData(table)
	NumberOfRow=len(StaffInfoList)
	newStaffList=[]
	for row in range(NumberOfRow):
		info=StaffInfoList[row]
		stuff_id=info[0]
		MaskedTC=CreateMaskedTC()
		MaskedSalary=CreateMaskedSalary(info[2])
		MaskedCreditCardNumber=CreateMaskedCCNumber(info[3])
		staff_info=(stuff_id,MaskedTC,MaskedSalary,MaskedCreditCardNumber)
		newStaffList.append(staff_info)
	return newStaffList

def NewMaskedDataTable():
	#Maskelenmiş tablo için yeni bir tablo oluşturarak maskeşenmiş verileri bu tabloya kaydeder
	createTable('masked_staff_info')
	newStaffList=MaskAllTable()
	conn=connectDb()
	c=conn.cursor()
	c.executemany('INSERT INTO masked_staff_info VALUES (?,?,?,?)', newStaffList)
	conn.commit()
	conn.close()

def menu():
  #Menü
  menu= """   
        ____________________MENÜ________________________

               1 => Verileri Maskele
               0 => Çıkış Yap                    
        ________________________________________________
            """
  print(menu,end='\n')

def menuSelection():
  #Kullanıcının Çıkış(0) dışında her işlemden sonra tekrar menüden seçim yapabilmesini sağlamak için while döngüsü kullanıldı.
  while True:
    menu()
    selection=input("Seçimin: ")
    if not selection:
      #Eğer kullanıcı hiçbir seçim yapmadan enter a basarsa çalışacak
      print("\aSeçim Yapmadın! Lütfen Gerçekleştirmek İstediğin İşlemin Numarasını Gir",end='\n\n')
      continue
    if selection== "1" :
      NewMaskedDataTable()
      print("Maskeleme İşlemi Tamamlandı")
    elif selection== "0" :  
      sys.exit()   #kullanıcı çıkış yapmak istediği takdirde programı sonlandıracak
    else:
      #Kullanıcı menüde belirtilen seçenek numaraları dışında başka bir numara girdiği takdirde çalışır
      print("\aLütfen Sadece Menüdeki Numaraları Gir",end='\n\n')


menuSelection()