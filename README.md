# MS Open Data - Simulation

Toto je ukazka analyzy dat, ktera byla ziskana ze simulatoru skoly.

## Jak to funguje

V simulatoru je vytvorena skola, do ktere chodi studenti, kteri jsou rozdeleni do jednotlivych skupin. Na skolu sviti slunce, jezdi okolo auta a fouka okolo ni vitr. Kazdy student zaroven produkuje teplo (jako v Matrixu) a hluk.

Skola ma senzory venku, ktere meri hluk, teplotu a silu vetru. Zaroven kazda trida ma senzory, ktere meri hluk a teplotu uvnitr tridy a pocet ptaku sedicich na parapetu.

Kod simulace je v souboru [simulation.py](simulation.py). Vysledkem simulace je cela rada souboru, ktere jsou ve sloze [data](data). Kazdy soubor obsahuje data z jednoho senzoru.

Aby se s daty dalo snadno pracovat, je nutne je spojit do jednoho souboru. To je ukol skriptu [preprocessing.py](proprocessing.py). Takto zpracovana data jsou ulozena v adresari [preprocessed](preprocessed).

## Jak muzete s temito daty pracovat

Bud je muzete zkusit zpracovat pomoci Google Sheetu - [https://goo.gl/cfUfzy](https://goo.gl/cfUfzy) - nebo pomoci Pythonu.

Vyhoda pouziti Pythonu je, ze to nevyzaduje zadne klikani a zaroven budete prohem produktivnejsi.

Ukazkova analyza dat je v souboru [Analysis.ipynb](Analysis.ipynb). Pokud si chces vyzkouset data analyzovat sam, mas nekolik moznosti:

* pouzit Microsoft Azure
* nainstalovat si Jupyter Notebook na vlastni pocitac
* pouzit demu od Jupyter Notebooku 

### Pouzit Microsoft Azure

Toto je nejjednodussi moznost jak si sam pohrat s daty.

1. Zajdi do [repozitare](https://notebooks.azure.com/martin-m/libraries/ms-open-data-simulation)
2. Vyber soubor Analysis.ipynb s nejvyssim cislem.
3. Klikni na Clone.
4. Vytvor si ucet podle instrukci.
5. Nyni si budes moci spustit a modifikovat jednotlive prikazy.

### Na vlastnim pocitaci

Nejdrive je nutne si nainstalovat Jupyter Notebook - [http://jupyter.org/install.html](http://jupyter.org/install.html). Vypada to, ze nejsnadnejsi je pouzit Anacodnu - [https://www.anaconda.com/download/](https://www.anaconda.com/download/) - a nainstalovat si verzi s Pythonem 3.6.

Po uspesne instalaci staci bud kopirovat prikazy z [Analysis.ipynb](Analysis.ipynb) nebo si tento soubor stahnout a nasledne otevrit.

### Try Jupyter

V tomto prostredi neni mozne stahnout soubor s daty, takze neni mozne cokoliv analyzovat.

1. Zajdi na [https://try.jupyter.org/](https://try.jupyter.org/)
2. V pravo nahore klikni na New a vyber Python 3
3. Je mozne spoustet prikazy.