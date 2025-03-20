#Martin Couture
#Mars 2025

from flask import Flask, make_response, render_template, request, redirect
import util.classeMeteo as clsMeteo
import time, asyncio
import util.jsonUtile as jsonUtil
app = Flask(__name__)
#Charge les normales JSON en mémoire au démarrage
jsonQuebec = jsonUtil.JSONUtil()
#Trouve la normale du jour
jsonNormalesDuJour = jsonQuebec.rechercheDate(time.strftime("%d"), time.strftime("%b"))

#Lecture de la météo en asynchrone
async def getMeteoQc():
    obsQuebec = clsMeteo.Meteo("https://meteo.gc.ca/rss/city/qc-133_f.xml") #Via la classe
    obsQuebec.lireMeteo() #Lecture de la météo actuelle pour la mise à jour
    return obsQuebec

#Chemin s'accès pour la météo
@app.route("/meteo")
async def formulaire():
    obsQuebec = await getMeteoQc() #Lecture de la météo via la méthode asynchrone.
    #Lecture des informations
    temperature = obsQuebec.temperature
    condition = obsQuebec.condition
    #Utilisation d'un template pour afficher les informations
    return render_template("meteo.html", temperature=temperature, condition=condition, date=time.strftime("%d-%b"),
                           normalesMin=jsonNormalesDuJour["min"], normalesMax=jsonNormalesDuJour["max"])

#Route de base est redirigée.
@app.route("/")
def index():
    return redirect("/meteo") #Redirection

#Pour transformer la date du formulaire en format pour la requête JSON
def dateTexte(date):
    dateList = date.split("-")
    mois = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    moisText = mois[int(dateList[1])-1]
    return [int(dateList[2]),moisText]

#Requête pour les normales
@app.route("/requetes", methods=["GET","POST"]) #L'option GET est ajoutée parce que lors du premier chargement la méthode est GET
def requetes():
    if request.method == "POST": #Par la suite les requêtes sont de type post.
        dateForm = time.strftime("%y-%m-%d") #Si le formulaire renvoi une date null.
        if request.form["date"]:
            dateForm = request.form["date"] #Sinon, prend la date du formulaire
        dateRecherche = dateTexte(dateForm)
        normalesRecherche = jsonQuebec.rechercheDate(dateRecherche[0], dateRecherche[1]) #Recherche dans le fichier JSON
        #Retourne le template avec les données lorsque POST
        return render_template("requetes.html", date=f"{dateRecherche[0]}-{dateRecherche[1]}",
                           normalesMin=normalesRecherche["min"], normalesMax=normalesRecherche["max"])
    else:
        # Retourne le template avec les données lorsque GET (avec les normales du jour courant)
        return render_template("requetes.html", date=time.strftime("%d-%b"),
                           normalesMin=jsonNormalesDuJour["min"], normalesMax=jsonNormalesDuJour["max"])

#Affiche la page 404 si besoin.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
