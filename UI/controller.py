import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI

        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self.selectedCountry = None
        self.selectedYear = None
        self.N = 0


    def fillDD(self):
        self._listYear = self._model.getListYear()
        self._listCountry = self._model.getListCountry()
        for c in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(text=c,
                                                                     data=c,
                                                                     on_click=self.readDDCountry))
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(text=y,
                                                                     data=y,
                                                                     on_click=self.readDDYear))


    def readDDCountry(self, e):
        if e.control.data is None:
            self.selectedCountry = None
        else:
            self.selectedCountry = e.control.data
        print(self.selectedCountry)

    def readDDYear(self, e):
        if e.control.data is None:
            self.selectedYear = None
        else:
            self.selectedYear = e.control.data
        print(self.selectedYear)

    def handle_graph(self, e):
        self._view.txt_result.clean()
        if self.selectedCountry is None or self.selectedYear is None:
            self._view.create_alert("Selezionare un anno e un paese")
        self._model.buildGraph(self.selectedYear, self.selectedCountry)
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha: {self._model.get_num_of_nodes()} nodi e: {self._model.get_num_of_edges()} archi"))
        self._view.update_page()




    def handle_volume(self, e):
        if self._model.get_num_of_nodes() == 0:
            self._view.create_alert("é necessario prima creare il grafo")
            return
        self._view.txtOut2.clean()
        self._model.calcolaVolumi()
        for x in self._model.get_volume_ret():
            self._view.txtOut2.controls.append(ft.Text(f"{x[0]} --> volume: {x[1]}"))

        self._view.update_page()


    def handle_path(self, e):
        self._view.txtOut3.clean()
        if self._model.get_num_of_nodes() == 0:
            self._view.create_alert("é necessario prima creare il grafo")
            return
        if self._model.volumi_calcolati is False:
            self._view.create_alert("Calcola i volumi prima")
            return
        if self._view.txtN.value == "":
            self._view.create_alert("Inserire una lunghezza di percorso superiore a 1")
            return
        self.N = int(self._view.txtN.value)
        print(self.N)
        if self.N<2:
            self._view.create_alert("Per creare il percorso servono almeno due vertici")
            return
        self._model.get_path(self.N)

        self._view.txtOut3.controls.append(ft.Text(f"Il percorso ha un peso totale di: {str(self._model.solBest)}"))

        for x in self._model.path_edges:
            self._view.txtOut3.controls.append(ft.Text(f"{x[0].Retailer_name} --> {x[1].Retailer_name} con peso di: {str(x[2])}"))

        self._view.update_page()
