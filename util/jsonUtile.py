import json
CHEMIN_FICHIER = "donnees/normales.json"
class JSONUtil:
    "Classe utilitaire JSON"
    def __init__(self):
        try:
            with open(CHEMIN_FICHIER, "r") as json_file:
                self.donneesJSON = json.load(json_file)



        except FileNotFoundError:
            print('Erreur de chargement du fichier JSON')
        except Exception as e:
            print(e)

    def rechercheDate(self, jour, mois):
        for donnee in self.donneesJSON:
            if donnee["Date"] == f"{jour}-{mois}":
                return donnee

    def recherchePdp(self, valeur, operateur):
        listePdp = []
        if operateur == ">":
            for donnee in self.donneesJSON:
                if float(donnee["pdp"]) > valeur:
                    listePdp.append(donnee)
        elif operateur == "<":
            for donnee in self.donneesJSON:
                if float(donnee["pdp"]) < valeur:
                    listePdp.append(donnee)
        elif operateur == "=":
            for donnee in self.donneesJSON:
                if float(donnee["pdp"]) == valeur:
                    listePdp.append(donnee)

        return listePdp



if __name__ == '__main__':
    j = JSONUtil()
    j.rechercheDate("2", "Apr")
    print(j.recherchePdp(0, "="))