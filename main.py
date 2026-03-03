# ============================================================
# API de predicció per sistema d'alarmes
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# ------------------------------------------------------------
# Crear aplicació FastAPI
# ------------------------------------------------------------
app = FastAPI(title="Servei de predicció - Alarma")

# ------------------------------------------------------------
# Carregar models i MAE base (només un cop)
# ------------------------------------------------------------
model_pot = joblib.load("model_potencia.pkl")
model_fp  = joblib.load("model_fp.pkl")
mae_pot_base = joblib.load("mae_pot_base.pkl")
mae_fp_base  = joblib.load("mae_fp_base.pkl")

# ------------------------------------------------------------
# Definir estructura de dades d'entrada
# Ha de coincidir amb les variables utilitzades al model (MODEL_FEATURES)
# ------------------------------------------------------------
class InputData(BaseModel):
    potencia: float
    potencia_lag1: float
    potencia_lag5: float
    potencia_lag30: float
    potencia_lag60: float
    potencia_lag120: float
    intensitat: float
    fp: float
    fp_lag1: float
    fp_lag30: float
    fp_lag60: float

# ------------------------------------------------------------
# Endpoint de predicció
# ------------------------------------------------------------
@app.post("/predict")
def predict(data: InputData):

    # Convertir entrada a DataFrame (una sola fila)
    input_df = pd.DataFrame([data.dict()])

    # Prediccions
    pot_pred = model_pot.predict(input_df)[0]
    fp_pred  = model_fp.predict(input_df)[0]

    # --------------------------------------------------------
    # Lògica d'alarma basada en MAE base
    # --------------------------------------------------------
    # Si la predicció difereix més que el MAE esperat, activem alarma
    alarma = 0
    if abs(pot_pred - data.potencia) > mae_pot_base:
        alarma = 1
    if abs(fp_pred - data.fp) > mae_fp_base:
        alarma = 1

    # Retornar resposta JSON
    return {
        "pot_pred": float(pot_pred),
        "fp_pred": float(fp_pred),
        "alarma": alarma
    }
