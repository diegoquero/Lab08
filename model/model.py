from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        self.load_impianti()
        lista_impianti = self._impianti
        lista_consumi = []
        lista_consumi_medi = []
        for impianto in lista_impianti:
            lista_consumo_impianto = impianto.get_consumi()
            for consumo in lista_consumo_impianto:
                if consumo.data.month == mese:
                    lista_consumi.append(consumo.kwh)
            media_consumo = sum(lista_consumi)/len(lista_consumi)
            lista_consumi_medi.append((impianto.nome,media_consumo))
        return lista_consumi_medi





    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """

        if giorno ==8:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
                print(self.__sequenza_ottima)
                print(self.__costo_ottimo)

        else:


            for i in consumi_settimana:
                nuovo_costo = costo_corrente
                if ultimo_impianto == i or ultimo_impianto == None:
                    nuovo_costo += (consumi_settimana[i][giorno-1])
                else:
                    nuovo_costo += (consumi_settimana[i][giorno-1] + 5)
                if sequenza_parziale is None:
                    sequenza_parziale = [consumi_settimana[i][giorno-1]]
                else:
                    nuova_sequenza_parziale = list(sequenza_parziale)
                    nuova_sequenza_parziale.append((i))
                ultimo_impianto = i
                self.__ricorsione(nuova_sequenza_parziale,
                                      giorno + 1,
                                      ultimo_impianto,
                                      nuovo_costo,
                                      consumi_settimana)







    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """

        dizionario_consumi_prima_settimana = {}
        for impianto in self._impianti:
            lista_consumi = []
            lista_consumo_impianto = impianto.get_consumi()
            for consumo in lista_consumo_impianto:
                if consumo.data.month == mese and consumo.data.day <=7:
                    if consumo.id_impianto==impianto.id:
                        lista_consumi.append(consumo.kwh)
            dizionario_consumi_prima_settimana.update({impianto.id: lista_consumi})
        print(dizionario_consumi_prima_settimana)
        return dizionario_consumi_prima_settimana




