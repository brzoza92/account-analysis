import pandas as pd
from datetime import datetime as dt


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
            
    def _getFileLength(self):
        """
        Returns the length of main file.
        """    
        self.length = self.main_file[self.main_file.columns[0]].count()
        return self.length
    def _columnsCmp(self, file_):
        """
        Compare amount of columns of files.
        """
        new_columns = file_.columns
        main_columns = list(self.columns)

        return len(main_columns) != len(new_columns)    
    
    def _columnsDiff(self, file_):
        """
        Returning the array with names of columns to be deleted out of new file.
        """
        new_columns_diff = len(file_.columns)
        main_columns_diff = len(list(self.columns))
        to_erease = list(range(main_columns_diff,new_columns_diff))
        to_erease_name = []
        for column in to_erease:
            to_erease_name.append(file_.columns[column])
        return to_erease_name  

    def _sortDictionary(self, InDictionary):
        tmp_list = sorted(InDictionary.items(), key=lambda x: x[1], reverse = False)
        result = {}
        for item in tmp_list:
            result[item[0]] = item[1]
        return result

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

    def ClearDuplicates(self):
        """
        Clears duplicates from file
        """
        file_ = self.ReadMain()
        file_.drop_duplicates(inplace = True)
        file_.to_csv(self.path, index = False, encoding=self.encoding)

        return None

    def NewData(self, newfile):
        """
        Adds new data logs from file path to a file used in instance of class. Cleares main file from duplicates.
        """
        try:
            df_new_data = pd.read_csv(newfile, encoding = self.encoding)

        except FileNotFoundError:
            print("Błąd. Brak pliku o podanej nazwie.")
            return False

        

        if self._columnsCmp(df_new_data):         #check if same type of csv data
            df_new_data.drop(columns = self._columnsDiff(df_new_data), inplace = True)
        
        df_new_data.to_csv(self.path, index = False, header = False, mode = 'a', encoding = self.encoding)
        
        self.ClearDuplicates()
        return True

    def Filtring(
        self, data, income = False, outcome = True,
        month = True, month_val = dt.now().month,
        year = True, year_val = dt.now().year,
        inside = False, category = False, category_val = "Spozywcze"):
        
        result = data
        if not (income and outcome):                         #selected only one option
            if income:
                result = result.loc[result[result.columns[3]] > 0]
            else:
                result = result.loc[result[result.columns[3]] < 0]

        
        if month:
            if (int(month_val) < 10):
                str_month = "-0{}-".format(month_val)
            else:
                str_month = "-{}-".format(month_val)
            result = result.loc[result[result.columns[0]].str.contains(str_month)]
            
        
        if year:
            str_year = "{}-".format(year_val)
            result = result.loc[result[result.columns[0]].str.contains(str_year)]
            
        
        if not inside:
            result = result.loc[result[result.columns[11]] != "Transfer wewnetrzny"]
        
        if category:
            result = result.loc[result[result.columns[11]] == category_val]
        return result    

    def SplitYears(self, income = False, outcome = True):
        """
        Presents costs taken in split for years.
        Income equal True to take both income and outcome in consideration
        """
        self.ReadMain()    
        years_dict = {}
        for year in range(2010, dt.now().year + 1):
            years_dict[year] = 0
        
        for y in years_dict:
            edited_file = self.Filtring(
                self.main_file, income = income, outcome = outcome,
                month = False, year = True, year_val = y
                )

            result = round(edited_file[edited_file.columns[3]].sum(), 2)
            if income:
                years_dict[y] = result
            else:
                years_dict[y] = result * -1  
        return years_dict

    def SplitMonths(self, year = dt.now().year, income = False, outcome = True):
        """
        Presents costs taken in split for months.

        During development add a year selection. In default, actual year.
        Income equal True to take both income and outcome in consideration
        """
        self.ReadMain()    

        months_dict = {}
        for month in range(1, 13):
            months_dict[month] = 0


        for m in months_dict:
            edited_file = self.Filtring(
                self.main_file, income = income, outcome = outcome,
                month_val = m, year_val = year
                )
            
            result = round(edited_file[edited_file.columns[3]].sum(), 2)
            if income:
                months_dict[m] = result
            else:
                months_dict[m] = result * -1 
        
        print(months_dict)
        return months_dict

    def SplitCategoriesMonthly(self, month = dt.now().month,
        year = dt.now().year, income = False, outcome = True):
        """
        Presents costs taken in split for categories in selected month.
        Income equal True to take both income and outcome in consideration
        """
        self.ReadMain()

        edited_file = self.Filtring(
            self.main_file, income = income, outcome = outcome,
            month_val = month, year_val = year
            )
        filter_cond_empty = edited_file[edited_file.columns[11]].isnull()
        if (edited_file.loc[filter_cond_empty][edited_file.columns[0]].count() > 0):
            print("Wystepują nieuzupełnione dane. Proszę uzupełnić")
            return None

        #generate dictionary of categories that occure in selected month
        cat_dictionary = {}
        for value in list(edited_file[edited_file.columns[11]]):
            cat_dictionary[value] = 0
        for category in cat_dictionary:
            cat_edited_file = self.Filtring(
                edited_file, income = income, outcome = outcome,
                month_val = month, year_val = year,
                category = True, category_val = category 
            )
            result = round(cat_edited_file[cat_edited_file.columns[3]].sum(), 2)
            if income:
                cat_dictionary[category] =  result
            else:
                cat_dictionary[category] =  result * -1 
                 
        return self._sortDictionary(cat_dictionary)


    def FindEmpty(self):
        """
        Returns index of account data table where there is no information
        about category of payment or place
        """
        categoryColumn = self.main_file[self.main_file.columns[11]]
        placeColumn = self.main_file[self.main_file.columns[12]]

        for row in range(0, self._getFileLength()):
            value_cat = str(categoryColumn[row])
            value_place = str(placeColumn[row])
            if  (value_cat or value_place) == "nan":
                return row
        return None   
    def IsFilled(self, index):
        """
        Returns if the record is filled with category and place name
        """
        self.ReadMain()
        categoryColumn_fill = self.main_file[self.main_file.columns[11]]
        placeColumn_fill = self.main_file[self.main_file.columns[12]]
        
        value_cat_fill = str(categoryColumn_fill[index])
        value_place_fill = str(placeColumn_fill[index])
        if  (value_cat_fill or value_place_fill) == "nan":
            return False
        else:  
            return True

    def FillCatAndPlace(self, index, category, place):
        """
        Loads prepared data into category and place of selected row of file
        """
        fill_file = self.ReadMain()   
        fill_file.at[index, fill_file.columns[11]] = category
        fill_file.at[index, fill_file.columns[12]] = place

        fill_file.to_csv(self.path, index = False, mode = 'w', encoding = self.encoding)
        return None

    def ClearCatAndPlace(self, index):
        """
        Clear category and place for selected record
        """
        self.ReadMain()   
        self.main_file.at[index, self.main_file.columns[11]] = "nan"
        self.main_file.at[index, self.main_file.columns[12]] = "nan"

        self.main_file.to_csv(self.path, index = False, mode = 'w', encoding = self.encoding)
        return None
       







