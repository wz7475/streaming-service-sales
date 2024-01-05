## Dokładność
**Błąd bezwględny** 
- jest liczony jako RMSE (Root Mean Square Error) jest to funkcja obliczająca różnicę między predykcją a prawdzinym wynikiem, błąd jest tego samego wielkość
rzędu co różnica wyników. Czym mniejszy błąd tym wyższa dokładność.

**Błąd względny** 
- jest iloczony jako iloraz błędu bezwględnego i sumy łącznego odtworzeń w danym okresie. Czym mniejszy błąd tym wyższa dokładność.
- jest wykorzystywany do porównywania dokładności modeli, czas odtworzeń różni w danym okresie dla danych artystów.

**Dokładność modeli**
- Dokładna analiza znajduje się w pliku `model/analyze_sarima_dummy.ipynb`
- Model złożony 
  - jest średnio 2.11 raza dokładniejszy od modelu prostego
  - w ok. 90% przypadków jest dokładniejszy od modelu prostego
  - średni błąd względny wynosi 1.6%. 
