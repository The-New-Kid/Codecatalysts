# crowd_model.py
import os
import joblib
import numpy as np
import pandas as pd
from datetime import date as date_cls

# Path to the pickle file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "ensemble_model_optionA.pkl")

# Load artifacts once at startup
artifacts = joblib.load(MODEL_PATH)
model_xgb = artifacts["model_xgb"]
m_prophet = artifacts["m_prophet"]
df_model = artifacts["df_model"]
alpha = artifacts.get("alpha", 0.7)

# ---------- Holiday Helper (same logic as your notebook) ----------
def get_holiday_value(full_date, day_name, festival):
    day_str = str(day_name).strip().lower()
    fest_str = str(festival or "").strip().lower()

    m = full_date.month
    d = full_date.day

    # Fixed holidays
    if (m == 1 and d == 1):      # New Year
        return 1
    if (m == 1 and d == 26):     # Republic Day
        return 1
    if (m == 8 and d == 15):     # Independence Day
        return 1
    if (m == 5 and d >= 15) or (m == 6):   # Summer holidays
        return 1
    if (m == 12 and d >= 25):    # Winter holidays
        return 1

    # Weekends
    if day_str in ["saturday", "sunday"]:
        return 1

    # Festival-based holidays
    holiday_festivals = [
        "new year",
        "republic",
        "republic day",
        "maha shivratri",
        "maha shivaratri",
        "holi",
        "independence",
        "independence day",
        "janmasthami",
        "janmashtami",
        "dusshera",
        "dussehra",
        "choti diwali",
        "chhoti diwali",
        "diwali",
        "govardhan",
        "govardhan puja",
        "bhaidooj",
        "bhai dooj",
        "bhaiya dooj"
    ]

    if any(key in fest_str for key in holiday_festivals):
        return 1

    return 0


def predict_crowd_for_date(year: int, month: int, day: int, festival_label: str = None) -> int:
    """
    Predict visitors for a single date using the trained Ensemble (XGBoost + Prophet).
    Uses last row of df_model for lag/rolling features (same as notebook).
    """

    # Build timestamp
    full_date = pd.Timestamp(year=year, month=month, day=day)
    weekday_name = full_date.strftime("%A")

    # Feature: holiday flag
    holidays_value = get_holiday_value(full_date, weekday_name, festival_label)

    # Festival flag
    fest_flag = 0 if str(festival_label or "Normal").lower() == "normal" else 1

    # Base features (weights chosen as 0.5 like in notebook)
    row = {
        "Date_Num": full_date.toordinal(),
        "Holidays": holidays_value,
        "Festival_Flag": fest_flag,
        "Month_sin": np.sin(2 * np.pi * full_date.month / 12),
        "Month_cos": np.cos(2 * np.pi * full_date.month / 12),
        "Daily Weight_Norm": 0.5,
        "Somnath Monthly weight_Norm": 0.5,
        "Somnath Festival Weight_Norm": 0.5,
    }

    row["festival_strength"] = row["Festival_Flag"] * row["Somnath Festival Weight_Norm"]

    # Lag & rolling features copied from last row (same trick as your predict_for_user_date)
    last = df_model.iloc[-1]
    for col in [
        "lag_1", "lag_2", "lag_3",
        "lag_7", "lag_14", "lag_30", "lag_60",
        "roll_7", "roll_30",
        "roll_7_std", "roll_30_std",
        "ewm_7", "ewm_30"
    ]:
        row[col] = last[col]

    # Build DataFrame in correct feature order
    xgb_input = pd.DataFrame([row])[model_xgb.get_booster().feature_names]

    # XGBoost prediction
    xgb_pred = float(model_xgb.predict(xgb_input)[0])

    # Prophet prediction
    prophet_df = pd.DataFrame({
        "ds": [full_date],
        "Holidays": [row["Holidays"]],
        "Festival_Flag": [row["Festival_Flag"]]
    })
    prophet_pred = float(m_prophet.predict(prophet_df)["yhat"].iloc[0])

    # Ensemble
    final_pred = alpha * xgb_pred + (1 - alpha) * prophet_pred

    return int(round(final_pred))