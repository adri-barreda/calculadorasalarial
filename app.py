from flask import Flask, request, jsonify, render_template
import os
import requests
import json
from PyPDF2 import PdfReader
import io

app = Flask(__name__)

def read_pdf(pdf_file):
    pdf_reader = PdfReader(io.BytesIO(pdf_file.read()))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')

    if file and file.filename.split('.')[-1] in ['pdf', 'txt']:
        if file.filename.split('.')[-1] == 'pdf':
            text = read_pdf(file)
        else:
            text = file.read().decode('utf-8')

        system_message = """Instrucciones
        Por favor, proporcione información en las siguientes categorías. Usaré una escala de 0-10 para cada uno de los primeros tres componentes. Los dos últimos componentes son factores multiplicadores.

        Educación y Certificaciones
        Sin educación formal: 0
        Educación Secundaria: 2
        Formación técnica o asociados: 4
        Licenciatura: 6
        Maestría: 8
        Doctorado o más: 10
        Certificaciones relevantes (añadir +1 por cada certificación relevante, hasta un máximo de +3)
        Experiencia Laboral
        Menos de 1 año: 1
        1-3 años: 3
        4-6 años: 5
        7-10 años: 7
        Más de 10 años: 10
        Habilidades Específicas
        Básicas: 2
        Intermedias: 5
        Avanzadas: 8
        Expertas: 10
        Ubicación (Factor multiplicador)
        Bajo costo de vida: 0.8
        Costo de vida medio: 1.0
        Alto costo de vida: 1.2
        Industria (Factor multiplicador)
        Baja demanda: 0.9
        Demanda media: 1.0
        Alta demanda: 1.1
        Cálculo Puntuación Total = ( Educación + Experiencia + Habilidades ) * Ubicación * Industria

        Rango Salarial Estimado
        Menor a 20: Salario bajo
        20-30: Salario medio-bajo
        30-40: Salario medio
        40-50: Salario medio-alto
        Mayor a 50: Salario alto
        Consejos para Negociar
        Se proporcionarán después de calcular el rango salarial estimado.

        Por favor, introduzca su Currículum y lo calcularemos en base a la información disponible:
        
        {}""".format(text)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
        }

        data = {
            'model': 'gpt-4',
            'messages': [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': 'Por favor, analice mi CV y proporcione un rango salarial estimado. Además, proporciona onsejos para negociar el salario. ES MUY IMPORTANTE QUE HAGA LOS CÁLCULOS BIEN, Y QUE ME COLOQUE EN EL RANGO SALARIAL AL QUE PERTENEZCO. TENGA EN CUENTA QUE EL MERCADO LABORAL ES EL ESPAÑOL, HAGA UNA ESTIMACIÓN EN BASE AL SALARIO ESPAÑOL.'}
            ]
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
        except Exception as e:
            return jsonify({'error': 'API request failed', 'detail': str(e)}), 500
        
        gpt_response = response.json()['choices'][0]['message']['content']

        return jsonify({'result': gpt_response})

    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)