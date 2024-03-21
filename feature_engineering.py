def feature_eng(data):
    # Menambahkan kolom Age_Category
    data['Age_Category'] = 0
    age = data['Age'][0]
    if age < 20:
        data['Age_Category'] = 1
    elif 20 <= age <= 24:
        data['Age_Category'] = 2
    elif 25 <= age <= 29:
        data['Age_Category'] = 3
    elif 30 <= age <= 34:
        data['Age_Category'] = 4
    elif 35 <= age <= 39:
        data['Age_Category'] = 5
    elif 40 <= age <= 44:
        data['Age_Category'] = 6
    elif 45 <= age <= 49:
        data['Age_Category'] = 7
    elif 50 <= age <= 54:
        data['Age_Category'] = 8
    elif 55 <= age <= 59:
        data['Age_Category'] = 9
    elif 60 <= age <= 64:
        data['Age_Category'] = 10
    elif 65 <= age <= 69:
        data['Age_Category'] = 11
    elif 70 <= age <= 74:
        data['Age_Category'] = 12
    elif 75 <= age <= 79:
        data['Age_Category'] = 13
    elif age > 79:
        data['Age_Category'] = 14

    # Menghapus kolom Age
    data.pop('Age')

    # Menambahkan kolom PolyInteraction
    data['PolyInteraction'] = data['Polyuria'][0] * data['Polydipsia'][0]

    return data