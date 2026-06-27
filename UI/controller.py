import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._categoriaUtente = None
        self._startPUtente = None
        self._endPUtente = None

    def fillDDCategorie(self):
        opzioni = self._model.getCategories()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(
            key=x.category_id,
            text=x.category_name,
            data=x,
            on_click=self._readChoice
        ), opzioni))
        self._view._ddcategory.options = opzioniDD

    def _readChoice(self, e):
        scelta = e.control.data

        if scelta is None:
            self._categoriaUtente = None

        else:
            self._categoriaUtente = scelta
            print(self._categoriaUtente)

    def handleCreaGrafo(self, e):
        categoria = self._categoriaUtente
        if categoria is None:
            self._view.create_alert('Selezionare una categoria')
            return
        startD = self._view._dp1.value
        if startD == "":
            self._view.create_alert('Selezionare una data di inzio')
            return
        endD = self._view._dp2.value
        if endD == "":
            self._view.create_alert('Selezionare una data di fine')
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Date selezionate:'))
        self._view.txt_result.controls.append(ft.Text(f'Start date: {startD}'))
        self._view.txt_result.controls.append(ft.Text(f'End date: {endD}'))
        self._model.creaGrafo(startD, endD, categoria.category_id)
        self._view.txt_result.controls.append(ft.Text(f'Grafo correttamente creato:', color='green'))

        nodi, archi = self._model.getInfo()
        self._view.txt_result.controls.append(ft.Text(f'Numero di nodi: {nodi}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di archi: {archi}'))

        self._fillDDProdotti()
        self._view.update_page()

    def _fillDDProdotti(self):
        opzioni = self._model.getNodi()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(
            key=x.product_id,
            text=x.product_name,
            data=x,
            on_click=self._readChoice1
        ), opzioni))
        self._view._ddProdStart.options = opzioniDD

        opzioniDD = list(map(lambda x: ft.dropdown.Option(
            key=x.product_id,
            text=x.product_name,
            data=x,
            on_click=self._readChoice2
        ), opzioni))
        self._view._ddProdEnd.options = opzioniDD

    def _readChoice1(self, e):
        scelta = e.control.data

        if scelta is None:
            self._startPUtente = None

        else:
            self._startPUtente = scelta
            print(self._startPUtente)

    def _readChoice2(self, e):
        scelta = e.control.data

        if scelta is None:
            self._endPUtente = None

        else:
            self._endPUtente = scelta
            print(self._endPUtente)

    def handleBestProdotti(self, e):
        best = self._model.getBestNodi()
        self._view.txt_result.controls.append(ft.Text(f'I cinque prodotti più venduti sono:'))
        for b in best:
            self._view.txt_result.controls.append(ft.Text(f'{b[0]} with score {b[1]}'))

        self._view.update_page()

    def handleCercaCammino(self, e):
        lun = self._view._txtInLun.value
        try:
            lunInt = int(lun)
            if lunInt < 0:
                raise Exception
        except:
            self._view.create_alert('Attenzione inserire un valore intero positivo!')
            return

        start = self._startPUtente
        if start is None:
            self._view.create_alert('Selezionare un prodotto di partenza')
            return
        end = self._endPUtente
        if end is None:
            self._view.create_alert('Selezionare un prodotto di arrivo')
            return

        self._view.txt_result.controls.clear()

        cammino, punteggio = self._model.getCamminoOttimo(start, end, lunInt)

        self._view.txt_result.controls.append(ft.Text(f'Il cammino ottimo ha peso {punteggio}', color='green'))
        for b in cammino:
            self._view.txt_result.controls.append(ft.Text(f'{b}'))

        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
