from flask import Flask, render_template, request
import os
import dill
import pandas as pd
import requests


app = Flask(__name__)
api_url = 'https://projet-7-bis.azurewebsites.net'


@app.route('/', methods=['GET', 'POST'])
def index():

    prediction = ""
    prediction_text = ""
    error_message = ""
    feedback_message = ""
    original_message = ""

    if request.method == 'POST':

        X = request.form.get('input_text')
        is_correct = request.form.get('is_correct')

        if X is not None:
            if len(X) > 280:
                error_message = "* Cette app ne prédit que les Tweets. Veuillez saisir un message de moins de 280 caractères."
            elif len(X) == 0:
                error_message = "* Veuillez saisir un message."
            else:
                # Send the text to the backend for processing and prediction
                response = requests.post(f'{api_url}/predict', json={'text': X})
                print(response.content)
                print(response.status_code)
                # Convert the response to a Python dictionary
                if response.content:
                    print("--------------------------------------------")
                    print(response.content)
                    print("--------------------------------------------")
                    try:
                        response_data = response.json()
                    except ValueError:
                        print("Response not in expected JSON format.")
                else:
                    print("Empty response received.")
                # Extract the original message and the prediction
                original_message = response_data['original_message']
                prediction = int(response_data['prediction'])

                prediction_text  = "Votre tweet a été prédit positif." if prediction == 1 else "Votre tweet a été prédit négatif."


        elif is_correct is not None:
            original_message_b = request.form.get('original_message')
            prediction = request.form.get('prediction')
            # Send the confirmation to the backend for processing
            response = requests.post(f'{api_url}/confirm', json={'is_correct': is_correct, 'original_message': original_message_b, 'prediction': prediction}, )
            if response.status_code == 200:
                feedback_message = ["Merci de votre feedback !", "Vous pouvez effectuer une nouvelle prédiction."]
            else:
                feedback_message = "Une erreur s'est produite lors de l'enregistrement de votre réponse."
            
            if os.path.exists('../results_api.dill'):
                with open('../results_api.dill', 'rb') as f:
                    df = dill.load(f)

                data_to_add = pd.DataFrame({'original_message': [original_message_b], 'prediction': [int(prediction)], 'confirmation': [is_correct]})
                df = pd.concat([df, data_to_add], ignore_index=True)
                with open('../results_api.dill', 'wb') as f:
                    dill.dump(df, f)
            else:
                df = pd.DataFrame({'original_message': [original_message_b], 'prediction': [int(prediction)], 'confirmation': [is_correct]})
                with open('../results_api.dill', 'wb') as f:
                    dill.dump(df, f)
            

    return render_template('index.html', error=error_message, prediction_text=prediction_text, feedback=feedback_message, original_message=original_message, prediction=prediction)

if __name__ == '__main__':
    app.run(port=8000, debug=True)