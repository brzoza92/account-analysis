# account-analysis
Analiza danych z prywatnego konta w banku PKO na podstawie pliku .csv wygenerowanego w serwisie.

Aplikacja daje możliwość dodania nowych wydatków oraz wgląd w historię wydatków, prezentowaną z wykorzystaniem diagramów.

Aby dodać nowe dane należy zapisać nowe dane w folderze aplikacji i po wybraniu odpowiedniej opcji w terminalu podać nazwę pliku, razem z rozszerzeniem .csv.

Możliwa jest prezentacja wydatków w podziale na lata kalendarzowe, na miesiące w konkretnym roku oraz na kategorie w wybranym miesiącu.

Dane dotyczące podziału wydatków na kategorie są zapisane w pliku dbFile.txt. Na podstawie tego pliku aplikacja szuka podobnego opisu transakcji i przypisuje jej kategorię. Jeżeli podobieństwo nie zostanie odnalezione użytkownik musi zdefiniować gdzie transakcja ma zostać przypisana. Po tej operacji opis tej transakcji jest dopisany do tej kategorii.

Wszystkie rekordy z konta są zapisane w pliku tabela.csv.

Funkcjonalności do dodania w przyszłośći:

- wykorzystanie konfiguratora filtrowania danych i prezentowanie danych na żądanie operatora, nie tylko podział jak powyżej.
- prezentowanie wyników nie tylko w formie diagramów, ale również poprzez wystawienie "dataFrame" w terminalu.




