import csv, operator
from operator import itemgetter
##Extraer nombre de pines, número y banco
with open("prueba/xc7z007sclg225pkg.csv")  as csvarchivos:
    entrada=csv.reader(csvarchivos)
    lista=[]
    for reg in entrada:
        lista.append(reg)
lista=lista[3:-2]
lista=sorted(lista, key=itemgetter(3))
pin=[]
pin_nam=[]
bank=[]
for i in range(len(lista)):
    pin.append(lista[i][0])
    pin_nam.append(lista[i][1])
    bank.append(lista[i][3])



zynq=["Zynq1"]
def num_capas():
    bank_prev=""
    cont=0
    banko=sorted(bank)
    for k in range(len(bank)):
        if bank_prev!=banko[k]:
            cont+=1
            bank_prev=banko[k]
    return cont

def num_pines(banco):
    return bank.count(banco)

#creador de pines
def create_pin():
    pin_kicad=""
    bank_prev=""
    capa=0
    visi='I'
    sq_y1=0
    sq_y2=0
    #init=400
    t=0
    ult_capa=0
    def pin_create(pin_nam, num_pin, pos_pin, capa, x='600',  long='150', dir='L', text_tam='50', num_tam='50', Morg='1', visi='I'):
        return "X "+str(pin_nam)+" " +str(num_pin)+ " " + x +" "+str(pos_pin)+ " "+ str(long)+ " " + str(dir) + " " + str(text_tam) + " " +str(num_tam) + " " + str(capa) + " " +str(Morg)+" " +str(visi)

    for j in range(len(pin)):

        ##Asignacion de capas
        t+=1
        if bank[j]!= bank_prev  :
            capa+=1
            if capa<num_capas():
                bank_prev=bank[j]
                t=0
                init=num_pines(bank[j])*50
                sq_y1=init+200
                sq_y2=-init-100
                pin_kicad+="\nS 450 "+ str(sq_y1) + " -600 " + str(sq_y2) + " " + str(capa) + " 1 0 f"
            elif capa==num_capas():
                if ult_capa==0:
                    t=0
                    #print("Entro1")
                    ult_capa=1
                    visi='W'
                    gnd=pin_nam.count("GND")
                    init=(gnd)*50
                    sq_y1=init+200
                    sq_y2=-init-100
                    pin_kicad+="\nS 450 "+ str(sq_y1) + " -600 " + str(sq_y2) + " " + str(capa) + " 1 0 f"
            else:
                capa=num_capas()+1
        if ult_capa==1:
            if pin_nam[j]=="GND":
                capa=num_capas()
                pin_nam_prev=1
            else:
                if pin_nam_prev==1:
                    print("entro2")
                    t=0
                    pin_nam_prev=0
                    capa=num_capas()+1
                    init=(num_pines(bank[j])-gnd)*50
                    print((num_pines(bank[j])-gnd)*50)
                    sq_y1=init+200
                    sq_y2=-init-100 
                    pin_kicad+="\nS 450 "+ str(sq_y1) + " -600 " + str(sq_y2) + " " + str(capa) + " 1 0 f"
            
        pin_kicad+="\n"+pin_create(pin_nam[j],pin[j], (init-t*100), capa, visi=visi)
    return pin_kicad


def longitud():
    lon_max=0
    cont=0
    for k in range(len(bank)):
        lon=bank.count(bank[k])
        #print(lon)
        if lon>lon_max:
            lon_max=lon
    return lon_max



#apertura de fichero
f=open("Zynq_prueba.lib", "w")


wr="EESchema-LIBRARY Version 2.4 \n#encoding utf-8"
dat=-int(longitud()*50+150)
#print(dat)
for i in zynq:
    wr+="\n#\n# "+i+"\n#"
    wr+="\nDEF "+i+" U 0 40 Y Y "+str(num_capas()+1)+" L N"
    wr+="\nF0  \"U\" -550 "+str(-dat+100)+" 50 H V C CNN"
    wr+="\nF1  \""+i+"\" -450 "+str(dat)+" 50 H V C CNN"
    wr+="\nF2  \"\" 0 "+str(dat)+" 50 H I C CNN"
    wr+="\nF3  \"\" 0 "+str(dat)+" 50 H I C CNN"
    wr+="\nDRAW"
    wr+=create_pin()
    wr+="\nENDDRAW"
    wr+="\nENDDEF"

wr+="\n#\n#End library"
#Escritura
f.write(wr)