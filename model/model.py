import networkx as nx

from database.DAO import DAO
class Model:
    def __init__(self):
        self.listYear = []
        self.listCountry = []

        self._graph = nx.Graph()
        self._nodes = []
        self._edges = []
        self.idMap = {}
        self.volumi_calcolati = False

    def getListYear(self):
        self.listYear = DAO.get_year()
        return self.listYear

    def getListCountry(self):
        self.listCountry = DAO.get_country()
        return self.listCountry

    def buildGraph(self, anno, paese):
        self._graph.clear()
        self._nodes.clear()
        self._edges.clear()
        retailer_list = DAO.get_retailers()
        for r in retailer_list:
            if r.Country == paese:
                self._nodes.append(r)

        self._graph.add_nodes_from(self._nodes)
        for n in self._nodes:
            self.idMap[n.Retailer_code] = n
            #print(n)

        self._edges = DAO.getSameProduct(anno, paese, self.idMap)
        print("Number of edges: ", len(self._edges))
        #for e in edges:
            #self._edges.append((e[0], e[1], e[2]['weight']))
            #print(e[0], e[1], e[2]['weight'])

        self._graph.add_weighted_edges_from(self._edges)

    def calcolaVolumi(self):
        self.volumi_calcolati = True
        self._volume_retailer = []
        self._retailer_connesso = []

        for n in self._graph.nodes:
            volume = 0
            for e in self._graph.edges(n, data = True):
                volume += e[2]['weight']
            if volume > 0:
                self._retailer_connesso.append((n))
                self._volume_retailer.append((n.Retailer_name, volume))
        self.volume_ret_sort = sorted(self._volume_retailer, key=lambda x: x[1], reverse=True)

    def get_path(self, N):
        self.path = []
        self.solBest = 0
        self.path_edges = []
        for r in self._retailer_connesso:
            partial = []
            partial.append(r)
            self.ricorsione(partial, N, [])

    def ricorsione(self, partial, N, partial_edge):
        r_last = partial[-1]
        r_first = partial[0]

        #condizione di terminazione
        if len(partial_edge) == (N-1):
            if self._graph.has_edge(r_last, r_first):
                partial_edge.append((r_last, r_first, self._graph.get_edge_data(r_last, r_first)['weight']))
                partial.append(r_first)
                weight_path = self.computeWeightPath(partial_edge)
                if weight_path > self.solBest:
                    self.solBest = weight_path
                    self.path = partial[:]
                    self.path_edges = partial_edge[:]
                partial.pop()
                partial_edge.pop()
            return

        neighbors = list(self._graph.neighbors(r_last))
        neighbors = [i for i in neighbors if i not in partial]
        for n in neighbors:
            partial_edge.append((r_last, n, self._graph.get_edge_data(r_last, n)['weight']))
            partial.append(n)

            self.ricorsione(partial, N, partial_edge)
            partial.pop()
            partial_edge.pop()






    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]
        return weight
    def get_nodes(self):
        return self._graph.nodes()

    def get_edges(self):
        return list(self._graph.edges(data=True))

    def get_volume_ret(self):
        return list(self.volume_ret_sort)
    def get_num_of_nodes(self):
        return self._graph.number_of_nodes()

    def get_num_of_edges(self):
        return self._graph.number_of_edges()
