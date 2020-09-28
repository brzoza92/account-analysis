from file_handling import File
from json_handling import dbFile
from plots import Chart

path = ""
new_account = File("tabela.csv")        
new_json = dbFile()
ploting = Chart()


print("Witaj,\nco chesz zrobić?")
print(
    "1 - dodaj nowe dane\n"
    "2 - odczytaj wyniki\n"
    "x - koniec\n"
)
selection1 = input()

while(True):

    if selection1 == "1":               #dodaj nowe dane
        print("Przenieś plik do folderu Account-analysis i podaj nazwę.")
        name_new_file = input("Nazwa: ")

        if new_account.NewData(name_new_file):
            #Filling category and place in data account file
            #================================================================
            #================================================================
            while(True):
                file = new_account.ReadMain()
                description1_column = file[file.columns[6]]
                description3_column = file[file.columns[2]]
                description2_column = file[file.columns[7]]
                cat_column = file[file.columns[11]]
                place_column = file[file.columns[12]]
                by_hand = False
                
                index = new_account.FindEmpty()
                if index is not None:
                    str_description = str(description2_column[index])
                    print(
                        '''
                        Opis transakcji:\n{descript3}\n{descript1}\n{descript}
                        '''.format(
                                descript3 = str(description3_column[index]),
                                descript1 = str(description1_column[index]),
                                descript = str_description
                                )
                        )
                    print(index)
                    auto_search = new_json.FindDescription(str_description)
                    if auto_search != []:
                        new_account.FillCatAndPlace(index, auto_search[0], auto_search[1])
                        print(
                            "Wybrano kategorie {} i miejsce o nazwie {}\n".format(
                                str(auto_search[0]), str(auto_search[1])
                                )
                            )
                    else:
                        by_hand = True
                        category = new_json.SelectCategory()
                        if category is None:
                            print("Błąd przy wyborze kategorii\n")
                            pass
                        else:
                            place_id = new_json.SelectPlaceIndex(category)
                            if place_id is None:
                                print("Błąd przy wyborze miejsca\n")    
                            else:
                                place = new_json.getPlaceNamebyIndex(place_id, category)
                                if place is None:
                                    print("Błąd przy wyborze miejsca\n")
                                    pass
                                else:
                                    print("Wybrano kategorie "+category +" i miejsce o nazwie "+place)
                                    new_account.FillCatAndPlace(index, category, place)
                                    new_json.AddDescriptionTarget(category, place_id, str_description)
                else:
                    print("Wszystkie dane wypelnione")
                    new_account.ClearDuplicates()
                    break
                if by_hand:
                    do_again = input("Kontynuowac? (y - tak), (n - nie)\n")
                    if do_again != "y":
                        new_account.ClearDuplicates()
                        break
            
            #==========================================================
            #==========================================================
        else:
            pass
    if selection1 == "2":               #odczytaj wyniki
        print("Co potrzebujesz?")
        print(
            "1 - Podział miesiąca na kategorie\n"
            "2 - Podział na miesiące\n"
            "3 - Podział na lata\n"
            "x - Wstecz\n"
        )
        selection2 = input()
        if selection2 == "1":   #podział na kategorie
            year_1 = int(input("Podaj rok:\n"))
            month_1 = int(input("\nPodaj miesiąc:\n"))

            if month_1 <= 12:

                ploting.Chart(
                    new_account.SplitCategoriesMonthly(month_1, year_1), 
                    label_X = "Koszty [PLN]", label_Y = "Kategoria",
                    title = "Wydatki z {miesiac}.{rok} w podziale na kategorie".format(miesiac = month_1, rok = year_1),
                    horizontal = True
                    )
        if selection2 == "2":   #podział na miesiące
            year_2 = int(input("Podaj rok:\n"))
            ploting.Chart(
                new_account.SplitMonths(year_2),
                label_X = "Miesiąc", label_Y = "Koszty [PLN]", 
                title = "Wydatki z {rok} w podziale na miesiące".format(rok = year_2),
                )
        if selection2 == "3":   #podział na lata
            ploting.Chart(
                new_account.SplitYears(),
                label_X = "Rok", label_Y = "Koszty [PLN]", 
                title = "Wydatki w podziale na lata",
                )
        else:                   #wstecz
            pass
    if not selection1.isnumeric():                 #koniec
        break
    print(
        "Coś jeszcze?\n"
        "1 - dodaj nowe dane\n"
        "2 - odczytaj wyniki\n"
        "x - koniec\n"
        )
    selection1 = input()
    if not selection1.isnumeric():      #koniec programu jeżeli inne niż cyfra
        break


