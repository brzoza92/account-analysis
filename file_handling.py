import pandas as pd

class File:
    def __init__(self):
        pass

    def Create(self, name):
        """
        Creates new data file using defined name. Name needs to have .csv suffix.
        """

        columns = {
            "Data operacji": 0, "Data waluty": 1,
            "Typ transakcji": 2, "Kwota": 3,
            "Waluta": 4, "Saldo po transakcji": 5,
            "Opis transakcji": 6, "Nazwa": 7, 
            "Tytuł": 8, "Info1": 9, "Info2": 10
        }
        df1 = pd.DataFrame(columns, index = [0])
        df1.to_csv(name, index = False, encoding="latin2")

