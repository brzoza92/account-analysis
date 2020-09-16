from file_handling import File


new_account = File("tabela1.csv")

#new_account.Create()

new_account.NewData("history_csv_20200914_182105.csv")
#new_account.NewData("history_csv_20200914_181117.csv")

#print(new_account.SplitMonths())


#print(new_account.ReadMain().head())