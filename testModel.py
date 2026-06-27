from model.model import Model

model = Model()

model.creaGrafo('2016-01-01', '2018-12-28', 7)
print('Grafo correttamente creato')

nodi, archi = model.getInfo() #Questa formattazione può variare in base all'esempio
print(f'Numero di nodi: {nodi}')
print(f'Numero di archi: {archi}')

print()
best = model.getBestNodi()
print(f'I cinque prodotti più venduti sono:')
for b in best:
    print(f'{b[0]} with score {b[1]}')

print()
prodotti = model.getNodi()
cammino, punteggio = model.getCamminoOttimo(prodotti[0], prodotti[-1], 4)
print(f'Il cammino ottimo ha un punteggio di {punteggio}')
for s in cammino:
    print(f'{s}')