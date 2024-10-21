# Documentatia proiectului

## Setup

1. Pentru a putea rula codul pe calculatorul propriu veti instala in python,dupa care un editor de cod vs code sau pycharm
2. Clonati proiectul de pe github folosind comanda in git bash : ***git clone https://github.com/FallenKing01/SyncSquadBackend.git***
3. Dupa ce ati instalat local proiectul ***trebuie sa instalati*** pachetele din fisierul ***requirements.txt*** cu comanda ***pip install -r requirements.txt***
4. Dupa ce toate pachetele au fost instalate veti putea rula proiectul cu comanda ***python app.py*** veti porni un server local unde veti putea vedea schimbarile facute

## Mod de lucru cu proiectul
### Arhitectura proiectului

Arhitectura proiectului este una simpla ce contine 2 layers: 
1. Layer 1 ***Controllers*** unde sunt toate endpointurile acestea nu trebuie sa contina logica!
2. Layer 2 ***Infratructure*** unde se fec atat verificarile inputurilor primite de api cat si partea de manipulare a bazei de date
3. Mai avem si un folder ***Domain*** unde avem 2 fisiere unul pentru extensii unde putem folosi jwt-pentru accesul la api sau salt-pentru criptarea parolei sau alte pachete...
4. Mai avem si un folder de ***Models*** unde se vor scrie toate inputurile endpointurilor(fiecare nou namespace va avea un file.py diferit) adica namespaceul de accounts va avea toate modelele care apartin de acest namespace
5. Folderul ***Utils*** unde vor fi fisiere cu functiile uitle sau alte fisiere pe care le vom considera necesare spre exemplu o functie ***Custom Exception***
6. Foarte inportant la final de proiect vom incerca sa facem secure apiul si sa folosim si env variables deci va fi necesar la un moment dat un file .env 
7. Daca instalati vreun pachet pe care il considerati necesar cu comanda pip install -nume pachet sa adaugati numele pachetului in fisierul de requirements.txt eventual cu versiunea instalata ex ***flask_cors==4.0.0*** vine de la ***pip install flask_cors==4.0.0***
### Mod de lucru cu githubul
1. Sa incercam pe cat posibil cand vom lucra fiecare sa aiba propriul branch numit cu numeledefamilie-dev adica spre exemplu al meu va fi alu-dev fiecare va avea branchul lui
2. In momentul cand am terminat cu un task pe care l-am facut vom da push la noi pe branch ***sa va fereasca bunutu sa dati pe main*** si apoi puteti crea un PR(PULL REQUEST) unde puneti la from branchul vostru si la to branchul care se va numi ***develop*** iar apoi asignati un coechipier sa va faca code review iar el va va accepta PR-ul daca codul este bun(adaugati comentarii daca e ceva suspect) si persoana care a facut PR-ul va trebui sa faca modificarile spuse iar procesul se repeta
3. Daca de exemplu cineva a lucrat la un task ar fi foarte bine sa nu faca schimbari in tot proiectul si apoi sa dea push pentru ca vor aparea foarte multe conflicte...astfel ***fiecare om din proiect va avea ca task un anumit namespace*** deci nu va trebui sa va atingeti de namespaceul altora!

## Comenzi utile pentru git 
Aici sunt cateva comenzi pe care le puteti folosi pana va obisnuiti cu ele daca nu v-ati obisnuit cu ele sa aveti in vedere aceasta sectiune : 
1. ***git branch*** -> vedeti brachurile locale pe care le aveti
2. ***git checkout -b nume-prenume/task-1***->crearea unui nou branch
3. ***git add .*** -> dati track la schimbarile pe care le-ati facut pe local pentru un eventual push pe main
4. ***git status*** -> vedeti la ce ati dat track in urma la git add
5. ***git checkout main*** -> cu comanda asta va mutati de pe un branch pe altul cuvantul main e un branch poate fi orice alt nume gen alu-dev
6. ***git branch -D nume-prenume/task-1*** ->stergerea branch de pe local
7. ***git pull origin main*** aduceti de pe local toate schimbarile de pe un anumit branch ***veti face asta de pe develop in fiecare zi***
8. ***git commit -m "TASK 2 | Gata si task-ul 2"*** faceti un commit unde explicati ***foarte scurt*** ce ati facut in acest commit 
9. ***git push origin alu-dev*** dati push pe propriul branch cu schimbarile realizate urmand sa faceti un PR catre develop

***PENTRU CEI CE NU DORESC SA SE COMPLICE CU COMENZI DIN CONSOLA*** EXISTA ***GITHUB DESKTOP*** SI TOTUL SE REALIZEAZA PRINTR-O ***INTERFATA PRIETENOASA***
