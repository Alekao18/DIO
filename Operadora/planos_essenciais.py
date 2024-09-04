def vitrine():
    vitrine = """\n
    ================================>Planos<======================================
    Plano Essencial Fibra-50Mbs(Recomendado para consumo médio de até 10GB)
    Plano Prata Fibra-100Mbs(Recomendado para um consumo médio acima de 10 GB até 20 GB.)
    Plano Premium Fibra-300Mbs(Recomendado para um consumo médio acima de 20 GB.)
    =============================================================================="""
    print(vitrine)
vitrine()

def recomendar_plano():
    consumo_medio=float(input('Qual o seu consumo médio mensal de internet?: '))
    if consumo_medio<=10:
        print('O plano ideal para você é o: Plano Essencial Fibra - 50Mbps')
    elif consumo_medio>10 and consumo_medio<=20:
        print('O plano ideal para você é o: Plano Prata Fibra - 100Mbps')
    else:
        print('O plano ideal para você é o: Plano Premium Fibra - 300Mbps')
    return(consumo_medio)
recomendar_plano()