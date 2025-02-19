from sklearn.neighbors import NearestNeighbors
import numpy as np
from .utils import prepare_match_data
from matrimonyapp.models import Profile, Register

def find_best_matches(reg_id, k=5):
    df, label_encoders, scaler = prepare_match_data()

    if reg_id not in df["reg_id"].values:
        return []

    total_users = len(df)
    if total_users < 2:
        return []  # Not enough users for matching

    # 🔹 Fetch user's caste and gender
    user_profile = Profile.objects.filter(reg_id=reg_id).first()
    user_register = Register.objects.filter(reg_id=reg_id).first()

    if not user_profile or not user_register:
        return []  # User profile or register entry not found

    user_caste = user_profile.caste
    user_gender = user_register.gender  # Get user's gender

    # 🔹 Match only female users from the same caste
    female_caste_users = Register.objects.filter(
        gender="Female",  # Only female profiles
        reg_id__in=Profile.objects.filter(caste=user_caste).values_list("reg_id", flat=True)  # Same caste
    ).values_list("reg_id", flat=True)

    # Ensure there are enough users for KNN
    same_caste_df = df[df["reg_id"].isin(female_caste_users)]

    if len(same_caste_df) < 2:
        return []  # Not enough female users in the same caste

    # Adjust k to fit available users
    k = min(k, len(same_caste_df) - 1)

    # Extract feature matrix and user data
    X = same_caste_df.drop(columns=["reg_id"]).values  # Exclude reg_id column
    user_index = same_caste_df[same_caste_df["reg_id"] == reg_id].index[0]
    user_vector = X[user_index].reshape(1, -1)

    # Train KNN model
    knn = NearestNeighbors(n_neighbors=k + 1, metric="euclidean")
    knn.fit(X)

    # Find nearest neighbors
    distances, indices = knn.kneighbors(user_vector)

    # Get matched user IDs (excluding the user itself)
    matched_user_ids = same_caste_df.iloc[indices[0][1:]]["reg_id"].tolist()

    return matched_user_ids
