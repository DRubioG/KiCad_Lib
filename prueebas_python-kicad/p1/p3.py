import csv, operator

with open("prueba/xc7z007sclg225pkg.csv")  as csvarchivos:
    entrada=csv.reader(csvarchivos)
    #print(entrada)
    lista=[]
    for reg in entrada:
        lista.append(reg)
        #del reg[0][:]
        #if reg[0]!=0:
       # print(reg[:2])
lista=lista[2:-2]
pin=[]
pin_nam=[]
bank=[]
for i in range(len(lista)-1):
    pin.append(lista[i+1][0])
    pin_nam.append(lista[i+1][1])
    bank.append(lista[i+1][3])
print(bank.count('501'))