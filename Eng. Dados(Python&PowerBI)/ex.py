#EXEMPLO
from datetime import date, datetime, time #biblioteca de data e tempo

d=date(2024, 8, 27)
print(d) #27/08/2024

print(date.today()) #.today traz a data atual

data_hora = datetime(2024, 8, 27)
print(data_hora) # Se vc não passar os valores opcionais (hora, minutos e segundos) ele apareçe zerado!

print(datetime.today()) # datetime.today traz a data e o tempo atual

hora = time(14, 46, 0)
print(hora) # Traz as horas