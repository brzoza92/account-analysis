import pandas as pd

class File:
    def __init__(self, name):
        """
        Initialization of class File. If called file is not existing, 
        then generates automatically one using own method Create.
        """
        self.path = name
        self.encoding = "latin2"
        
        try:
            self.ReadMain()

        except FileNotFoundError:
            pass
            print("File is not existing yet.")
            self.Create()
            

    def ReadMain(self):
        """
        Shortcut method to read main file.
        """

        self.main_file = pd.read_csv(self.path, encoding=self.encoding)
        return self.main_file
    
    def Create(self):
        """
        Creates new data file using instance name. Name needs to have .csv suffix.
        """

        self.columns = {
            "Data operacji": 0, "Data waluty": 1,
            "Typ transakcji": 2, "Kwota": 3,
            "Waluta": 4, "Saldo po transakcji": 5,
            "Opis transakcji": 6, "Nazwa": 7, 
            "Tytuł": 8, "Info1": 9, "Info2": 10
        }
        df1 = pd.DataFrame(self.columns, index = [0])
        df1.drop(axis = 0, index = df1.index[0], inplace = True)
        df1.to_csv(self.path, index = False, encoding=self.encoding)

        

    def NewData(self, newfile):
        """
        Adds new data logs from file path to a file used in instance of class. Cleares main file from duplicates.
        """
        
        df_new_data = pd.read_csv(newfile, encoding = self.encoding)
        df_new_data.to_csv(self.path, index = False, header = False, mode = 'a', encoding = self.encoding)
        
        self.ReadMain()     #Main file needs to be read again (refreshed) after writing to file done above.
        self.main_file.drop_duplicates(inplace = True)
        self.main_file.to_csv(self.path, index = False, encoding = self.encoding)
