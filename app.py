from flask import Flask, render_template, request, jsonify

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form/prediksi', methods=["GET", "POST"])
def predict():
    try:
        if request.method == "POST":
            # Mendapatkan data dari request POST
            data = request.json

            # Menyesuaikan data dengan feature engineering yang telah diterapkan pada data training
            data['Age_Category'] = 0
            if (data['Age'][0] >= 16) & (data['Age'][0] <= 25):
                data['Age_Category'] = 1
            elif (data['Age'][0] > 25) & (data['Age'][0] <= 35):
                data['Age_Category'] = 2
            elif (data['Age'][0] > 35) & (data['Age'][0] <= 45):
                data['Age_Category'] = 3
            elif (data['Age'][0] > 45) & (data['Age'][0] <= 55):
                data['Age_Category'] = 4
            elif (data['Age'][0] > 55) & (data['Age'][0] <= 65):
                data['Age_Category'] = 5
            elif (data['Age'][0] > 65) & (data['Age'][0] <= 75):
                data['Age_Category'] = 6
            elif (data['Age'][0] > 75) & (data['Age'][0] <= 85):
                data['Age_Category'] = 7
            elif data['Age'][0] > 85:
                data['Age_Category'] = 8

            data.pop('Age')
            data['PolyInteraction'] = data['Polyuria'][0] * data['Polydipsia'][0]

            # Konversi ke DataFrame
            data_df = pd.DataFrame(data)

            # le = LabelEncoder()
            # df['class'] = le.fit_transform(df['class'])

            # Pilih hanya kolom numerik untuk transformasi
            numeric_columns = data_df.select_dtypes(include=[np.number]).columns
            data_numeric = data_df[numeric_columns]

            # Menerapkan transformasi PCA pada data baru
            scaler = StandardScaler()
            new_data_std = scaler.transform(data_numeric)
            pca = PCA(n_components=14)
            new_data_pca = pca.transform(new_data_std)

            # Prediksi terhadap data baru
            prediction = model.predict(new_data_pca)
            predicted_class = prediction[0]
            # predicted_class_original = le.inverse_transform([predicted_class])[0]

            return render_template('prediksi.html', prediction_text = "{}".format(predicted_class))

        return render_template('prediksi.html', prediction_text="Negative")
        
    except Exception as e:
        return jsonify({'error': str(e)})
