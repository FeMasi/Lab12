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
        self._volume_retailer = []
        self._retailer_connesso = []

        for n in self._graph.nodes:
            volume = 0
            for e in self._graph.edges(n, data = True):
                volume += e[2]['weight']
            if volume > 0:
                #self._retailer_connesso.append((n))
                self._volume_retailer.append((n.Retailer_name, volume))
        self.volume_ret_sort = sorted(self._volume_retailer, key=lambda x: x[1], reverse=True)



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
