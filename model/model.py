import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._IDMap = {}

        self._bestCammino = []
        self._bestPunteggio = 0

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategories()
    
    def creaGrafo(self, start, end, categoria):
        self._grafo.clear()
        self._IDMap = {}

        nodi = DAO.getNodi(categoria)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._IDMap[n.product_id] = n

        archi = DAO.getArchi(categoria, start, end, self._IDMap)
        for a in archi:
            self._grafo.add_edge(a[0], a[1], weight=a[2])

    def getNodi(self):
        return list(self._grafo.nodes())

    def getInfo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getBestNodi(self):
        nodi = []
        for n in list(self._grafo.nodes()):
            archiEntranti = list(self._grafo.in_edges(n, data=True))
            archiUscenti = list(self._grafo.out_edges(n, data=True))

            sommaE = sum([d['weight'] for u,v,d in archiEntranti])
            sommaU = sum([d['weight'] for u, v, d in archiUscenti])

            punteggio = sommaU - sommaE
            nodi.append((n, punteggio))

        nodi.sort(key=lambda x: x[1], reverse=True)
        return nodi[:5]

    def getCamminoOttimo(self, start, end, soglia):
        #OCCHIO CHE IL PESO DIPENDE DAL PESO QUINDI MAGARI POSSO OTTIMIZZARE
        self._bestCammino = []
        self._bestPunteggio = 0

        parziale = [start]
        self._ricorsione(parziale, end, soglia)

        return self._bestCammino, self._bestPunteggio

    def _ricorsione(self, parziale, end, soglia):
        ''' CONTROLLO PRIMA SE SONO ALLA FINE, POI NEL CASO CALCOLO I SUCCESSORI '''
        if parziale[-1] == end:
            if len(parziale) > len(self._bestCammino):
                self._bestCammino = copy.deepcopy(parziale)
                self._calcolaKm(parziale)
            return

        validi = self._getSuccessors(parziale, soglia, end)

        for n in validi:
            parziale.append(n)
            self._ricorsione(parziale, end, soglia)
            parziale.pop()

    def _getSuccessors(self, parziale, soglia, end):
        ''' END DEVE ESSERE MESSO A PRESCRINDERE QUINDI GLIELO PASSO E LO INSERISCO'''
        succ = self._grafo.neighbors(parziale[-1])
        validi = []

        for n in succ:
            if n not in parziale:
                if n == end or n.stars > soglia:
                    validi.append(n)

        return validi

    def _calcolaKm(self, parziale):
        ''' IL GRAFO AVEVA COME PESO LA DISTANZA QUINDI LA CALCOLIAMO COME PESO DELL'ARCO '''
        distanza = 0

        for p in range(len(parziale) - 1):
            u = parziale[p]
            v = parziale[p + 1]
            distanza += self._grafo[u][v]['weight']

        self._bestKm = distanza