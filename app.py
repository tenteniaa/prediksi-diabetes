from flask import Flask, render_template, request

import pandas as pd
import pickle

app = Flask(__name__)
model_LR = pickle.load(open('model_LR.pkl', 'rb'))
le = pickle.load(open('le.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
pca = pickle.load(open('pca.pkl', 'rb'))

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

@app.route('/form/prediksi')
def predict():
    return render_template('prediksi.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        form_values = request.form.to_dict()

        data = {}

        for key, value in form_values.items():
            try:
                new_value = float(value)
                data[key] = [new_value]
            except ValueError:
                print(f"Warning: Nilai '{value}' pada atribut '{key}' tidak dapat diubah menjadi float.")

        # Lakukan sesuatu dengan data, misalnya, prediksi menggunakan model machine learning
        data['Age_Category'] = 0
        if data['Age'][0] <= 15:
            data['Age_Category'] = 1
        elif (data['Age'][0] > 15) & (data['Age'][0] <= 25):
            data['Age_Category'] = 2
        elif (data['Age'][0] > 25) & (data['Age'][0] <= 35):
            data['Age_Category'] = 3
        elif (data['Age'][0] > 35) & (data['Age'][0] <= 45):
            data['Age_Category'] = 4
        elif (data['Age'][0] > 45) & (data['Age'][0] <= 55):
            data['Age_Category'] = 5
        elif (data['Age'][0] > 55) & (data['Age'][0] <= 65):
            data['Age_Category'] = 6
        elif (data['Age'][0] > 65) & (data['Age'][0] <= 75):
            data['Age_Category'] = 7
        elif (data['Age'][0] > 75) & (data['Age'][0] <= 85):
            data['Age_Category'] = 8
        elif data['Age'][0] > 85:
            data['Age_Category'] = 9
        data.pop('Age')
        data['PolyInteraction'] = data['Polyuria'][0] * data['Polydipsia'][0]

        data_df = pd.DataFrame(data)

        new_data_std = scaler.transform(data_df)
        # new_data_pca = pca.transform(new_data_std)

        # Prediksi terhadap data baru
        prediction = model_LR.predict(new_data_std)
        predicted_class = prediction[0]
        predicted_class_original = le.inverse_transform([predicted_class])[0]

        return render_template('prediksi.html', prediction_text=predicted_class_original)

    # Jika metode bukan POST, tampilkan halaman formulir
    return render_template('form.html')
