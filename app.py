from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import pandas as pd
import google.generativeai as genai
from datetime import timedelta
from data import initial_documents  # Importando o array initial_documents

app = Flask(__name__)
app.secret_key = 'AIzaSyBRvSVWy5zOcZES9KvWg9DCTxnRi9fr4nA'

# Configuração do Google GenAI
GOOGLE_API_KEY = "GOOGLE_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

df = pd.DataFrame(initial_documents)
df.columns = ['Titulo', 'Conteudo']
model = "models/embedding-001"

# calculando os embeddings
def embed_fnc(title, text):
    return genai.embed_content(model=model,
                               content=text,
                               title=title,
                               task_type="RETRIEVAL_DOCUMENT")["embedding"]

df["Embeddings"] = df.apply(lambda row: embed_fnc(row["Titulo"], row["Conteudo"]), axis=1)

# realizando a consulta na base de dados
def buscar_consulta(consulta, base, model):
    embedding_da_consulta = genai.embed_content(model=model,
                                                content=consulta,
                                                task_type="RETRIEVAL_QUERY")["embedding"]
    produtos_escalares = np.dot(np.stack(df["Embeddings"]), embedding_da_consulta)
    indice = np.argmax(produtos_escalares)
    return df.iloc[indice]["Conteudo"]

generation_config = {
    "temperature": 0.5,
    "candidate_count": 1
}

def zerar_historico():
    session.pop('historico', None)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    session.modified = True

historico = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'historico' not in session:
        session['historico'] = []

    if request.method == 'POST':
        consulta = request.form['consulta']
        trecho = buscar_consulta(consulta, df, model)
        prompt = f"Reescreva de uma maneira formal: {trecho}"
        model_2 = genai.GenerativeModel("gemini-1.0-pro", generation_config=generation_config)
        response = model_2.generate_content(prompt)
        session['historico'].append((consulta, response.text))
        return render_template('index.html', historico=session['historico'], documentos=df.to_dict('records'))

    return render_template('index.html', historico=session['historico'], documentos=df.to_dict('records'))

@app.route('/limpar_historico', methods=['POST'])
def limpar_historico():
    zerar_historico()
    return redirect(url_for('index'))

@app.route('/novo_item', methods=['GET', 'POST'])
def novo_item():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        new_row = {'Titulo': titulo, 'Conteudo': conteudo}
        df.loc[len(df)] = new_row
        df['Embeddings'] = df.apply(lambda row: embed_fnc(row["Titulo"], row["Conteudo"]), axis=1)
        return redirect(url_for('index'))

    return render_template('novo_item.html')

if __name__ == '__main__':
    app.run(debug=True)
