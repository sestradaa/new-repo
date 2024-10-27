from flask import Flask, render_template
#render_template renderiza un template(pagina html), para
#eso busca una carpeta q se llame template

#creando instancia
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


#iniciando el servidor, debug true hace q el codigo 
# se modifique solo en el navegador
if __name__ == '__main__':
    app.run(debug=True)