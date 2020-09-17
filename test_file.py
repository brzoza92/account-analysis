from file_handling import File, dbFile


new_account = File("tabela2.csv")

#new_account.Create()

#new_account.NewData("history_csv_20200914_182105.csv")
#new_account.NewData("history_csv_20200914_181117.csv")

#rint(new_account.SplitMonths())


#print(new_account.ReadMain().head())

new_json = dbFile()
#new_json.AddPlace()

print(new_json.getPlaceNamebyIndex(1, "Spozywcze"))



