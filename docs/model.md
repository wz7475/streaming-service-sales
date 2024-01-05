# Dokumentacja - Model

## Założenia

W celu modelowania czasu odsłuchiwania artysty przyjęto założenie, że czas
artysty jest określony jako średni czas otworzenia jednego utworu pomnożony
przez liczbę odtworzeń w danym okresie (miesiącu). Do modelowania zastosowano
agregację danych zamiast zakładanej tygodniowej.

## Model

Dla każdego artysty tworzone są dwa niezależne modele - naiwny oraz złożony.

### Model naiwny

Model naiwny opiera się na średniej z ostatnich czterech miesięcy.

### Model złożony

Model złożony został skonstruowany przy użyciu algorytmu SARIMA, z dobranymi
eksperymentalnie hiperparametrami. Przeprowadzono analizę strojenia
hiperparametrów dla każdego artysty indywidualnie, dla klastrów artystów oraz
dla wszystkich artystów łącznie. Ostatecznie zdecydowano się na strojenie
hiperparametrów dla wszystkich artystów, jednak tworzenie modelu dla każdego
artysty osobno.

## Spostrzeżenia

### Wykorzystanie agregacji tygodniowej zamiast miesięcznej

Zastosowanie agregacji miesięcznej umożliwia znacznie szybsze strojenie
hiperparametrów, co obejmuje również potencjalne rozszerzenie o automatyczne
strojenie, oraz aktualizacje lub cykliczne ponowne generowanie modeli. Mimo że
możliwe jest wykorzystanie agregacji tygodniowej, wymaga to użycie większych
zasobów obliczeniowych i pamięciowych. Obecny zestaw modeli opartych
o agregację miesięczną waży w przybliżeniu 9 GB.

### Sieci rekurencyjne

Chociaż do implementacji modelu złożonego można było wykorzystać sieci
rekurencyjne, ich stopień skomplikowania oraz czas potrzebny do treningu byłby
znacznie wyższy niż w przypadku używanego algorytmu SARIMA. Zgodnie z
literaturą, sieci rekurencyjne mogłyby jednak pozwolić na uzyskanie jeszcze
dokładniejszych predykcji, pomimo wyższego nakładu czasowego na proces
treningu.

## Możliwości rozbudowy

### Aktualizacja modelu w czasie działania serwisu

Warto zauważyć, że wykorzystywane biblioteki oraz sposób definicji modelu
naiwnego pozwalają na elastyczną rozbudowę serwisu. Możliwe jest dokonywanie
aktualizacji modeli w trakcie działania serwisu, eliminując konieczność
ponownego trenowania modeli od początku. Dzięki temu serwis może dostosowywać
się do zmieniających się warunków rynkowych oraz nowych danych, co przyczynia
się do zwiększenia precyzji prognoz.