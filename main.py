from flask import Flask, render_template, request
from feature_engineering import feature_eng

import pandas as pd
import pickle

app = Flask(__name__)

model_LR = pickle.load(open('./models/model_LR.pkl', 'rb'))
le = pickle.load(open('./models/le.pkl', 'rb'))
scaler = pickle.load(open('./models/scaler.pkl', 'rb'))
pca = pickle.load(open('./models/pca.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

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

        # Feature Engineering pada 'Age' dan PolyInteraction
        data = feature_eng(data)

        data_df = pd.DataFrame(data)

        new_data_std = scaler.transform(data_df)
        new_data_pca = pca.transform(new_data_std)

        # Prediksi terhadap data baru
        prediction = model_LR.predict(new_data_pca)
        predicted_class = prediction[0]
        predicted_class_original = le.inverse_transform([predicted_class])[0]

        return render_template('prediksi.html', prediction_text=predicted_class_original)

    # Jika metode bukan POST, tampilkan halaman formulir
    return render_template('form.html')

@app.route('/model')
def model():
    # Baca dataset dari file CSV
    dataset = pd.read_csv('./dataset/diabetes_early.csv')
    
    # Ubah dataset menjadi list of dictionaries agar mudah ditampilkan di HTML
    data = dataset.to_dict('records')
    
    return render_template('model.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
