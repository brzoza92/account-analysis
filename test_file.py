from file_handling import File
from json_handling import dbFile

new_account = File("tabela3.csv")

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



#Filling category and place in data account file
#================================================================
while(True):
    file = new_account.ReadMain()
    description1_column = file[file.columns[6]]
    description2_column = file[file.columns[7]]
    cat_column = file[file.columns[11]]
    place_column = file[file.columns[12]]
    by_hand = False
    
    index = new_account.FindEmpty()
    if index is not None:
        print(
            "Opis transakcji:\n" 
            +str(description1_column[index]) +"\n"
            +str(description2_column[index]) + "\n"
            )
        print(index)
        auto_search = new_json.FindDescription(description2_column[index])
        if auto_search != []:
            new_account.fillCatAndPlace(index, auto_search[0], auto_search[1])
            print("Wybrano kategorie "+str(auto_search[0]) +" i miejsce o nazwie "+str(auto_search[1])+"\n")
        else:
            by_hand = True
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
                        new_json.AddDescriptionTarget(category, place_id, description2_column[index])
    else:
        print("Wszystkie dane wypelnione")
        break
    if by_hand:
        do_again = input("Kontynuowac? (y - tak), (n - nie)\n")
        if do_again != "y":
            break
    
#==========================================================
#==========================================================

#Capturing description from data account file and saving into json file
#==========================================================
while(False):    
    file = new_account.ReadMain()
    file_length = file[file.columns[0]].count()
    done = False
    for row in range (0, file_length):
        if new_account.IsFilled(row):
            description = file[file.columns[7]][row]
            category = file[file.columns[11]][row]
            place = file[file.columns[12]][row]
            id_place = new_json.getPlaceIndexByName(place, category)
            if id_place is not None:
                new_json.AddDescriptionTarget(category, id_place, description)
            else:
                print("Problem z wierszem o numerze " +str(row)+"\n")
                new_account.ClearCatAndPlace(row)
                break
        if (row == (file_length - 1)):
            done = True
    if not done:          
        do_again2 = input("Kontynuowac? (y - tak), (n - nie)\n")
        if do_again2 != "y":
            break
    else:
        break
#==========================================================
#==========================================================


