"""
set FLASK_APP=main.py
export FLASK_DEBUG=1
$env:FLASK_APP = "main.py"
flask run --reload
"""
from flask import Flask, make_response, render_template, request, redirect
import util.objMeteo as objMeteo
import time, asyncio
import util.jsonUtile as jsonUtil
app = Flask(__name__)

jsonQuebec = jsonUtil.JSONUtil()
jsonNormalesDuJour = jsonQuebec.rechercheDate(time.strftime("%d"), time.strftime("%b"))

#Lecture de la météo en asynchrone
async def getMeteoQc():
    obsQuebec = objMeteo.Meteo("https://meteo.gc.ca/rss/city/qc-133_f.xml")
    obsQuebec.lireMeteo()
    return obsQuebec

#Chemin s'accès pour la météo
@app.route("/meteo")
async def formulaire():
    obsQuebec = await getMeteoQc()
    temperature = obsQuebec.temperature
    condition = obsQuebec.condition

    return render_template("meteo.html", temperature=temperature, condition=condition, date=time.strftime("%d-%b"),
                           normalesMin=jsonNormalesDuJour["min"], normalesMax=jsonNormalesDuJour["max"])

#Route de base est redirigée.
@app.route("/")
def index():
    return redirect("/meteo")
'''
# @app.route("/usager/<nom>")
# def getUsager(nom):
#     return render_template("base.html", nom=nom)
#     #reponse = make_response('<h1>Allo {}</h1>'.format(id))
#     #return reponse

# @app.route("/add", methods=["POST"])
# def add():
#     nom = request.form['nom']
#     with open("data.txt", "a") as file:
#         file.write(f"{nom}\n")
#
#     return redirect("/formulaire")
'''
#Affiche la page 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
