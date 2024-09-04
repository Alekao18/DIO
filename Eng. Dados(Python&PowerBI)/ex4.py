import pytz
from datetime import datetime, timezone, timedelta

# Fuso Horários

data = datetime.now(pytz.timezone('Europe/Oslo'))
data2 = datetime.now(pytz.timezone('America/Sao_Paulo')) # Importando horarios diferentes

print(data)
print(data2)

data3 = datetime.now(timezone(timedelta(hours=2))) # timezone com datetime
data4 = datetime.now(timezone(timedelta(hours=-3)))

print(data3)
print(data4)