#Utilitaire pour lire le JSON
import json
CHEMIN_FICHIER = "donnees/normales.json" #Constante pour le fichier
#Classe
class JSONUtil:
    "Classe utilitaire JSON"
    #Initialisation de la classe et lecture du fichier pour une mise en mémoire.
    def __init__(self):
        try:
            with open(CHEMIN_FICHIER, "r") as json_file:
                self.donneesJSON = json.load(json_file)
        #Exceptions
        except FileNotFoundError:
            print('Erreur de chargement du fichier JSON')
        except Exception as e:
            print(e)
    #Méthode pour la recherche d'une date
    def rechercheDate(self, jour, mois):
        for donnee in self.donneesJSON:
            if donnee["Date"] == f"{jour}-{mois}":
                return donnee
    #Méthode pour la recherche pour les probabilités de précipitation.
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


#Quelques éléments pour tester.
if __name__ == '__main__':
    j = JSONUtil()
    j.rechercheDate("2", "Apr")
    print(j.recherchePdp(0, "="))