import pandas as pd
import json

class File:
    def __init__(self, name):
        """
        Initialization of class File. If called file is not existing, 
        then generates automatically one using own method Create.
        """
        self.path = name
        self.encoding = "latin2"
        self.columns = {
            "Data operacji": 0, "Data waluty": 1,
            "Typ transakcji": 2, "Kwota": 3,
            "Waluta": 4, "Saldo po transakcji": 5,
            "Opis transakcji": 6, "Nazwa": 7, 
            "Tytuł": 8, "Info1": 9, "Info2": 10, 
            "Kategoria": 11, "Placówka": 12
        }


        try:
            self.ReadMain()

        except FileNotFoundError:
            pass
            print("File is not existing yet.")
            self.Create()
            
    def __getMonthDict__(self):
        """
        Reinitialize dictionary of months. 
        """
        self.months = {}
        for i in range(1,13):
            if i < 10:
                month_no = "0"+str(i)
            else:
                month_no = str(i)
            month_no = "-"+ month_no + "-"
            self.months[month_no] = 0
        return self.months
    def __getFileLength__(self):
        """
        Returns the length of main file.
        """    
        self.length = self.main_file[self.main_file.columns[0]].count()
        return self.length
    def __columnsCmp__(self, file):
        """
        Compare amount of columns of files.
        """
        new_columns = file.columns
        main_columns = list(self.columns)

        return len(main_columns) != len(new_columns)    
    
    def __columnsDiff__(self, file):
        """
        Returning the array with names of columns to be deleted out of new file.
        """
        new_columns_diff = len(file.columns)
        main_columns_diff = len(list(self.columns))
        to_erease = list(range(main_columns_diff,new_columns_diff))
        to_erease_name = []
        for column in to_erease:
            to_erease_name.append(file.columns[column])
        return to_erease_name  

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
        df1 = pd.DataFrame(self.columns, index = [0])
        df1.drop(axis = 0, index = df1.index[0], inplace = True)
        df1.to_csv(self.path, index = False, encoding=self.encoding)

        return None

    def NewData(self, newfile):
        """
        Adds new data logs from file path to a file used in instance of class. Cleares main file from duplicates.
        """
        
        df_new_data = pd.read_csv(newfile, encoding = self.encoding)

        if self.__columnsCmp__(df_new_data):         #check if same type of csv data
            df_new_data.drop(columns = self.__columnsDiff__(df_new_data), inplace = True)
        
        df_new_data.to_csv(self.path, index = False, header = False, mode = 'a', encoding = self.encoding)
        
        self.ReadMain()     #Main file needs to be read again (refreshed) after writing to file done above.
        self.main_file.drop_duplicates(inplace = True)
        self.main_file.to_csv(self.path, index = False, encoding = self.encoding)


        return None
    def SplitMonths(self):
        """
        Presents costs taken in split for months.

        During development add a year selection. In default, actual year.
        """
        self.__getMonthDict__()
        self.ReadMain()    

        #invest = ["revolut", "brzozowski"]

        dateColumn = self.main_file[self.main_file.columns[0]]
        amountColumn = self.main_file[self.main_file.columns[3]]
        #transName = self.main_file[self.main_file.columns[7]]
        for m in self.months:
            sum = 0
            rows = []
            for value in range(0, self.__getFileLength__()):
                if (m in dateColumn[value]) and (amountColumn[value] < 0):
                    # if any(cond in transName[value].lower() for cond in invest):
                    #     pass
                    # else:
                    rows.append(value)    #save what row fits to condition above
            for ids in rows:
                sum += amountColumn[ids]
            self.months[m] =  round(sum,2) * -1      
        
        return self.months

class dbFile:
    def __init__(self):
        """
        Initialization of class handling the json file with data to sort acount values for type and place name
        """
        self.file_name = "dbFile.txt"
        self.categories = "categories"

        try:
            self.__Open__()

        except FileNotFoundError:
            pass
            print("File is not existing yet.")
            self.__Create__()

    def __Open__(self):
        """
        Opens the dbFile
        """
        with open(self.file_name, 'r') as infile:
            self.file = json.load(infile)

        return self.file    

    def __Write__(self, data):
        """
        Writes the dbFile
        """
        with open(self.file_name, 'w') as outfile:
            json.dump(data, outfile, indent = 4)

        return None    

    def __Create__(self):
        """
        Creating of default file in case if the file is lost.
        """
        default_data = {}
        default_data[self.categories] = [
            "Spozywcze", "Rachunki", "Paliwo", "Restauracje",
            "Odziez", "Platnosc przez internet", "Dla psa"
            ]
        for category in default_data[self.categories]:
            default_data[category] = []
            default_data[category].append({"Nazwa placowki": "", "Opis transakcji": []})

        self.__Write__(default_data)

        return None

    def __getCategoriesList__(self):
        file = self.__Open__()
        return file[self.categories]

    def __getDefDictKeys__(self, data):
        return list(data[0].keys())

    def selectCategory(self):
        """
        Returns string with selected category, to search through dictionary
        """
        print("Lista kategorii:")
        categories = self.__getCategoriesList__()
        for i,j in enumerate(categories):
            print(str(i) + "- " + j)
        category = int(input("Wybierz kategorie: "))
        return categories[category]

    def selectPlace(self, category):
        """
        Returns index of dictionary with selected place
        """

        file_place = self.__Open__()

        names_key = self.__getDefDictKeys__(file_place[category])[0]
        i = 0
        for dict in file_place[category]:
            if i > 0:
                print(str(i) +"- " +dict.get(names_key))
            i += 1    
        if (i >= 2):
            place = int(input("Wybierz miejsce: "))       
        else:
            print("Brak placówek. Musisz dodać miejsca do kategorii " + category)
            place = 0
        return place

    def AddCategory(self):
        """
        Adding of category to json file
        """

        new_category = input("Podaj nazwe kategorii: ")
        update_category = self.__Open__()
        update_category[self.categories].append(new_category)

        self.__Write__(update_category)

        return None

    def AddPlace(self):
        """
        Adding new place in specified category
        """
        update_attributes = self.__Open__()
        category = self.selectCategory()
        
        
        new_name = input("Podaj nazwe miejsca: ")

        section = update_attributes[category]
        new_dict = {self.__getDefDictKeys__(section)[0]: new_name, self.__getDefDictKeys__(section)[1]: []}
        section.append(new_dict)

        self.__Write__(update_attributes)
        return None

    def AddDescription(self):
        """
        Adding new description for specified place
        """
        update_description = self.__Open__()
        category = self.selectCategory()
        key = self.__getDefDictKeys__(update_description[category])[1]
        place = self.selectPlace(category)
        if place > 0:
            new_description = input("Podaj opis: ")
            update_description[category][place].get(key).append(new_description)

            self.__Write__(update_description)
        return None
