# 🏠 Airbnb Madrid — Price Predictor API

A Flask REST API that predicts Airbnb nightly prices in Madrid using a Random Forest Regressor trained on Inside Airbnb data.

---

## 👥 Team

- Edu
- Ariela

---

## 🤖 Model

- **Algorithm:** Random Forest Regressor (sklearn)
- **Dataset:** Inside Airbnb — Madrid (detailed listings)
- **Features:** neighbourhood, room type, accommodates, bathrooms, bedrooms, beds, minimum nights, number of reviews, review scores rating, availability
- **R² Score:** 0.61 | **MAE:** €27 | **RMSE:** €37

---

## 🚀 API Endpoints

| Method | Route | Type | Description |
|--------|-------|------|-------------|
| GET | `/health` | — | Returns API status and model load confirmation |
| GET | `/predict/<neighbourhood>` | Path param | Quick price estimate for a given neighbourhood |
| GET | `/listings?room_type=entire` | Query param | Returns listings filtered by room type |
| POST | `/predict` | JSON body | Full price prediction using all features |

---

## 📨 Example Request

```bash
POST /predict
Content-Type: application/json

{
  "neighbourhood_cleansed": "Embajadores",
  "room_type": "Entire home/apt",
  "accommodates": 2,
  "bathrooms": 1,
  "bedrooms": 1,
  "beds": 1,
  "minimum_nights": 2,
  "number_of_reviews": 45,
  "review_scores_rating": 4.8,
  "availability_365": 180
}
```

## 📨 Example Response

```json
{
  "predicted_price": 116.11
}
```

---

## 🛠️ Run Locally

1. Clone the repository
```bash
git clone https://github.com/Speakful/airbnb-madrid-api.git
cd airbnb-madrid-api
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
python app.py
```

4. API will be available at `http://127.0.0.1:5000`

---

## ☁️ Deployment

Deployed on **Render**. Public URL: `coming soon`

---

## 🧰 Tech Stack

- Python
- Flask
- scikit-learn
- pandas
- joblib
- gunicorn
- Render
