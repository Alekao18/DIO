from datetime import datetime

data_hora_atual = datetime.now()
data_hora_str = "2023-10-20 10:20"
mascara = "%d/%m/%Y %a" # modelo de data brasileiro
mascara2 = "%Y-%m-%d %H:%M"

print(data_hora_atual.strftime(mascara)) 

print(datetime.strptime(data_hora_str, mascara2)) # convertendo uma string em data

