import json

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
        while(True):
            categories = self.__getCategoriesList__()
            for i,j in enumerate(categories):
                print(str(i) + "- " + j)
            category = input("Wybierz kategorie. (n - dodaj nowa), (x - przerwij)\n")
            if category.isdigit():
                return categories[int(category)]
            else: 
                if category == 'n':
                    self.AddCategory()
                else: 
                    break
        return None        
    def selectPlaceIndex(self, category):
        """
        Returns index of dictionary with selected place
        """
        while(True):
            file_place = self.__Open__()
            names_key = self.__getDefDictKeys__(file_place[category])[0]
            i = 0
            for dict in file_place[category]:
                if i > 0:
                    print(str(i) +"- " +dict.get(names_key))
                i += 1    
            if (i >= 2):
                place = input("Wybierz miejsce. (n - dodaj nowe), (x - przerwij)\n")   
            else:
                place = input("Brak placówek w kategorii "+ category +". (n - dodaj nowe), (x - przerwij)\n" )
            if place.isdigit():
                return int(place)
            else: 
                if place == 'n':
                    self.AddPlace()
                else: 
                    break
        return None

    def getPlaceNamebyIndex(self, index, category):
        """
        Returns place name selected by category and it's index in category
        """
        file_placeName = self.__Open__()
        names_key = self.__getDefDictKeys__(file_placeName[category])[0]
        try:
            placeName = file_placeName[category][index].get(names_key)
            return placeName
        except IndexError:
            print("Brak pozycji pod tym numerem")
            return None

    def AddCategory(self):
        """
        Adding of category to json file
        """

        new_category = input("Podaj nazwe kategorii: ")
        update_category = self.__Open__()
        update_category[self.categories].append(new_category)

        update_category[new_category] = []
        update_category[new_category].append({"Nazwa placowki": "", "Opis transakcji": []})


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
        place = self.selectPlaceIndex(category)
        if place > 0:
            new_description = input("Podaj opis: ")
            update_description[category][place].get(key).append(new_description)

            self.__Write__(update_description)
        return None

    def SetTypeAndPlace(self, description):
        print ("Opis transakcji: " + description)
        # category = dbFile.selectCategory(self)
        # place_index =  dbFile.selectPlaceIndex(self)
        # place = dbFile.getPlaceNamebyIndex(self, place_index)
