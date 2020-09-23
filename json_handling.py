import json
import difflib

class dbFile:
    def __init__(self):
        """
        Initialization of class handling the json file with data to sort acount values for type and place name
        """
        self.file_name = "dbFile.txt"
        self.categories = "categories"

        try:
            self._Open()

        except FileNotFoundError:
            pass
            print("File is not existing yet.")
            self.__Create__()

    def _Open(self):
        """
        Opens the dbFile
        """
        with open(self.file_name, 'r') as infile:
            self.file = json.load(infile)

        return self.file    

    def _Write(self, data):
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

        self._Write(default_data)

        return None

    def _getCategoriesList(self):
        file = self._Open()
        return file[self.categories]

    def _getDefDictKeys(self, data):
        return list(data[0].keys())

    def SelectCategory(self):
        """
        Returns string with selected category, to search through dictionary
        """
        print("Lista kategorii:")
        while(True):
            categories = self._getCategoriesList()
            for i,j in enumerate(categories):
                print("{}- {}".format(i, j))
            category = input("Wybierz kategorie. (n - dodaj nowa), (x - przerwij)\n")
            if category.isdigit():
                return categories[int(category)]
            else: 
                if category == 'n':
                    self.AddCategory()
                else: 
                    break
        return None        
    def SelectPlaceIndex(self, category):
        """
        Returns index of dictionary with selected place
        """
        while(True):
            file_place = self._Open()
            names_key = self._getDefDictKeys(file_place[category])[0]
            i = 0
            for dictionary in file_place[category]:
                if i > 0:
                    print("{} - {}".format(i, dictionary.get(names_key)))
                i += 1    
            if (i >= 2):
                place = input("Wybierz miejsce. (n - dodaj nowe), (x - przerwij)\n")   
            else:
                place = input("Brak placówek w kategorii {}. (n - dodaj nowe), (x - przerwij)\n".format(category))
            if place.isdigit():
                return int(place)
            else: 
                if place == 'n':
                    self.AddPlace()
                else: 
                    break
        return None

    def getPlaceIndexByName(self, place, category):
        """
        Returns place index in category selected by category and it's name 
        """
        file_placeIndex = self._Open()
        try:
            names_keyIndex = self._getDefDictKeys(file_placeIndex[category])[0]
            for id_Index, data in enumerate(file_placeIndex[category]):
                if (data.get(names_keyIndex) == place):
                    return id_Index

        except KeyError:
            return None       

    def getPlaceNamebyIndex(self, index, category):
        """
        Returns place name selected by category and it's index in category
        """
        file_placeName = self._Open()
        names_key = self._getDefDictKeys(file_placeName[category])[0]
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
        update_category = self._Open()
        update_category[self.categories].append(new_category)

        update_category[new_category] = []
        update_category[new_category].append({"Nazwa placowki": "", "Opis transakcji": []})


        self._Write(update_category)

        return None

    def AddPlace(self):
        """
        Adding new place in specified category
        """
        update_attributes = self._Open()
        category = self.SelectCategory()
        
        
        new_name = input("Podaj nazwe miejsca: ")

        section = update_attributes[category]
        new_dict = {self._getDefDictKeys(section)[0]: new_name, self._getDefDictKeys(section)[1]: []}
        section.append(new_dict)

        self._Write(update_attributes)
        return None

    def AddDescription(self):
        """
        Adding new description with selecting category and place.

        Add arguments, if present arguments of category and place then skip selecting
        """
        update_description = self._Open()
        category = self.SelectCategory()
        key = self._getDefDictKeys(update_description[category])[1]
        place = self.SelectPlaceIndex(category)
        if place > 0:
            new_description = input("Podaj opis: ")
            update_description[category][place].get(key).append(new_description)

            self._Write(update_description)
        return None

    def AddDescriptionTarget(self, category, index, description):
        update_description_target = self._Open()
        key_description = self._getDefDictKeys(update_description_target[category])[1]
        description_list = update_description_target[category][index].get(key_description)
        if description not in description_list:
            update_description_target[category][index].get(key_description).append(description)

            self._Write(update_description_target)

    def FindDescription(self, description_text):
        find_description_file = self._Open()
        categories = find_description_file[self.categories]

        for category in categories:             #search through each category
            for dictionary_id in range(0, len(find_description_file[category])):        #search through each dict
                close_match = []
                place_name = []
                descriptions_list = []
                place_name = list(find_description_file[category][dictionary_id].values())[0]
                descriptions_list = list(find_description_file[category][dictionary_id].values())[1]
                close_match = difflib.get_close_matches(
                    str(description_text),
                    descriptions_list, n = 1,
                    cutoff = 0.98
                    )
                if close_match != []:
                    self.AddDescriptionTarget(category, dictionary_id, description_text)
                    return [category, place_name]
        print("Nie znaleziono podobnego opisu transakcji\n")
        return []            

