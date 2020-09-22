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

    def __sortDictionary__(self, InDictionary):
        tmp_list = sorted(InDictionary.items(), key=lambda x: x[1], reverse = True)
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
        file = self.ReadMain()
        file.drop_duplicates(inplace = True)
        file.to_csv(self.path, index = False, encoding=self.encoding)

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

    def SplitYears(self):
        """
        Presents costs taken in split for years.
        """
        self.ReadMain()    
        years_dict = {}
        for year in range(2010, dt.now().year + 1):
            years_dict[year] = 0
        dateColumn = self.main_file[self.main_file.columns[0]]
        amountColumn = self.main_file[self.main_file.columns[3]]
        for y in years_dict:
            filter_cond = (
                dateColumn.str.contains(str(y)+"-")
                & (amountColumn < 0)
                )
            edited_file = self.main_file.loc[filter_cond]
            #print(edited_file[edited_file.columns[0]])
            result = round(edited_file[edited_file.columns[3]].sum(), 2)
            years_dict[y] = result * -1 
        return years_dict

    def SplitMonths(self, year):
        """
        Presents costs taken in split for months.

        During development add a year selection. In default, actual year.
        """
        self.__getMonthDict__()
        self.ReadMain()    

        year_str = str(year) + "-"
        dateColumn = self.main_file[self.main_file.columns[0]]
        amountColumn = self.main_file[self.main_file.columns[3]]
        for m in self.months:
            filter_cond = (
                dateColumn.str.contains(year_str)
                & dateColumn.str.contains(m)
                & (amountColumn < 0)
                )
            edited_file = self.main_file.loc[filter_cond]
            result = round(edited_file[edited_file.columns[3]].sum(), 2)
            self.months[m] = result * -1 
        
        return self.months

    def SplitCategoriesMonthly(self, month, year):
        """
        Presents costs taken in split for categories in selected month.
        """
        self.ReadMain()
        if month < 10:
            str_month = "0" + str(month)
        else:
            str_month = str(month)
        date_str = str(year)+ "-" + str_month + "-"    
        dateColumn = self.main_file[self.main_file.columns[0]]
        amountColumn = self.main_file[self.main_file.columns[3]]
        catColumn = self.main_file[self.main_file.columns[11]]

        #generate dictionary of categories that occure in selected month
        cat_dictionary = {}
        filter_cond = (
            dateColumn.str.contains(date_str)
            & (amountColumn < 0)
            )
        filter_cond_empty = (filter_cond & catColumn.isnull())
        if (self.main_file.loc[filter_cond_empty][self.main_file.columns[0]].count() > 0):
            print("Wystepują nieuzupełnione dane. Proszę uzupełnić")
            return None

        edited_file = self.main_file.loc[filter_cond]
        #generate dictionary of categories that occure in selected month
        for value in list(edited_file[edited_file.columns[11]]):
            cat_dictionary[value] = 0
        for category in cat_dictionary:
            cat_edited_file = edited_file.loc[edited_file[edited_file.columns[11]] == category] 
            result = round(cat_edited_file[cat_edited_file.columns[3]].sum(), 2)
            cat_dictionary[category] =  result * -1      
        return self.__sortDictionary__(cat_dictionary)


    def FindEmpty(self):
        """
        Returns index of account data table where there is no information
        about category of payment or place
        """
        categoryColumn = self.main_file[self.main_file.columns[11]]
        placeColumn = self.main_file[self.main_file.columns[12]]

        for row in range(0, self.__getFileLength__()):
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

    def fillCatAndPlace(self, index, category, place):
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
       







