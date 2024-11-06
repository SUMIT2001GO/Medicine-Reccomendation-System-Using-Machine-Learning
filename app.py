from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the data
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(medicine):
    print("Selected Medicine:", medicine)  # Debugging print
    if medicine not in medicines['Drug_Name'].values:
        return []  # Return an empty list if the medicine is not found
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
    return recommended_medicines

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_medicine_name = None
    if request.method == 'POST':
        selected_medicine_name = request.form['medicine']
        print("Form Medicine:", selected_medicine_name)  # Debugging print
        recommendations = recommend(selected_medicine_name)
    return render_template('index.html', medicines=medicines['Drug_Name'].values, recommendations=recommendations, selected_medicine_name=selected_medicine_name)

if __name__ == '__main__':
    app.run(debug=True)
