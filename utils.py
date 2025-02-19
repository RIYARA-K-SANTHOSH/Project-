import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from matrimonyapp.models import Register, Profile, Education

def prepare_match_data():
    users = Register.objects.filter(blocked=False).select_related("profile")

    data = []
    label_encoders = {}  # For categorical encoding

    for user in users:
        try:
            profile = user.profile
            education = Education.objects.filter(reg_id=user).first()

            row = {
                "reg_id": user.reg_id,  # Changed from "user_id" to "reg_id"
                "age": profile.age if profile.age else 0,
                "height": float(profile.height) if profile.height else 0,
                "weight": float(profile.weight) if profile.weight else 0,
                "mother_tongue": profile.mother_tongue,
                "caste": profile.caste,
                "education_level": education.degree_name if education else "None",
                "annual_income": int(profile.annual_income) if profile.annual_income else 0,
                "marital_status": profile.marital_status
            }
            data.append(row)
        except Profile.DoesNotExist:
            continue

    df = pd.DataFrame(data)

    # Encode categorical variables
    categorical_cols = ["mother_tongue", "caste", "education_level", "marital_status"]
    for col in categorical_cols:
        label_encoders[col] = LabelEncoder()
        df[col] = label_encoders[col].fit_transform(df[col].astype(str))

    # Normalize numeric features
    scaler = StandardScaler()
    numeric_cols = ["age", "height", "weight", "annual_income"]
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df, label_encoders, scaler
