from file_handling import File
from json_handling import dbFile

new_account = File("tabela2.csv")

#new_account.Create()

#new_account.NewData("history_csv_20200914_182105.csv")
#new_account.NewData("history_csv_20200914_181117.csv")

#rint(new_account.SplitMonths())


#print(new_account.ReadMain().head())
new_json = dbFile()
#new_json.AddPlace()

# category = new_json.selectCategory()

# place_index = new_json.selectPlaceIndex(category)

# print(new_json.getPlaceNamebyIndex(place_index, category))

while(True):
    file = new_account.ReadMain()
    description1_column = file[file.columns[6]]
    description2_column = file[file.columns[7]]
    cat_column = file[file.columns[11]]
    place_column = file[file.columns[12]]
    
    index = new_account.FindEmpty()
    if (index >= 0):
        print(
            "Opis transakcji:\n" 
            +description1_column[index] +"\n"
            +description2_column[index] + "\n"
            )
        print("indeks = "+str(index))
        category = new_json.selectCategory()
        if category is None:
            print("Błąd przy wyborze kategorii\n")
            pass
        else:
            place_id = new_json.selectPlaceIndex(category)
            if place_id is None:
                print("Błąd przy wyborze miejsca\n")    
            else:
                place = new_json.getPlaceNamebyIndex(place_id, category)
                if place is None:
                    print("Błąd przy wyborze miejsca\n")
                    pass
                else:
                    print("Wybrano kategorie "+category +" i miejsce o nazwie "+place)
                    new_account.fillCatAndPlace(index, category, place)

    else:
        print("Wszystkie dane wypelnione")
        break
    do_again = input("Kontynuowac? (y - tak), (n - nie)\n")
    if do_again != "y":
        break
    
