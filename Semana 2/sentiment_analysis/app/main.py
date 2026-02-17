import os
from flask import Flask, request, render_template, session, redirect
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from google.oauth2 import id_token
from google.auth.transport import requests as grequests

from sentiment import analizar_sentimiento
from text_utils import (
    normalizar_texto,
    es_solo_simbolos,
    es_texto_basura,
    tiene_palabras_validas,
    PALABRAS_GENERICAS
)

# ==============================
# CONFIGURACIÓN APP
# ==============================

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
ALLOWED_DOMAIN = "gmail.com"  # Cambia esto por tu dominio de Workspace si es necesario

# ==============================
# VALIDAR TOKEN GOOGLE
# ==============================

def verify_google_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )

        # Validar dominio Workspace
        if idinfo.get("hd") != ALLOWED_DOMAIN:
            return None

        return idinfo

    except Exception as e:
        print("Error validando token:", e)
        return None


# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    token = data.get("credential")

    user_info = verify_google_token(token)

    if user_info:
        session["user"] = {
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "picture": user_info.get("picture")
        }
        return {"status": "success"}
    else:
        return {"status": "unauthorized"}, 401


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ==============================
# RUTA PRINCIPAL
# ==============================

@app.route("/", methods=["GET", "POST"])
def analizar_estados():

    # GET → Mostrar login o formulario
    if request.method == "GET":
        return render_template(
            "index.html",
            client_id=GOOGLE_CLIENT_ID,
            user=session.get("user")
        )

    # POST → Validar sesión
    if "user" not in session:
        return redirect("/")

    archivo = request.files["file"]
    df = pd.read_excel(archivo)

    if df.shape[1] != 1:
        return "El archivo debe tener una sola columna", 400

    serie = df.iloc[:, 0].dropna().astype(str)
    serie = serie.apply(normalizar_texto)
    serie = serie[~serie.isin(PALABRAS_GENERICAS)]
    serie = serie[~serie.apply(es_solo_simbolos)]
    serie = serie[~serie.apply(es_texto_basura)]
    serie = serie[serie.apply(tiene_palabras_validas)]

    sentimientos = serie.apply(analizar_sentimiento)

    resultado_df = pd.DataFrame({
        "comentario": serie.values,
        "sentimiento": sentimientos.values
    })

    conteo = resultado_df["sentimiento"].value_counts()
    total = conteo.sum()
    porcentajes = (conteo / total * 100).round(1)

    colores = {
        "Positivo": "#4CAF50",
        "Neutral": "#BDBDBD",
        "Negativo": "#E53935"
    }

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(conteo.index, conteo.values,
                  color=[colores[i] for i in conteo.index])

    for bar, p in zip(bars, porcentajes):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.2,
            f"{p}%",
            ha="center",
            weight="bold"
        )

    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format="png")
    img.seek(0)
    grafico = base64.b64encode(img.getvalue()).decode()

    excel = BytesIO()
    resultado_df.to_excel(excel, index=False)
    excel.seek(0)
    excel_b64 = base64.b64encode(excel.getvalue()).decode()

    return render_template(
        "result.html",
        total=total,
        grafico=grafico,
        excel=excel_b64,
        user=session.get("user")
    )


# ==============================
# RUN CLOUD RUN
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
