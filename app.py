from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import random
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
from scipy.stats import gaussian_kde
import io
import base64

app = Flask(__name__)

# Configuración de la sesión
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

global_acumulador = 0
resultados_globales = []

def ListaSimulaciones(lanzamientos, simulaciones):
    dado1 = [1, 2, 3, 4, 5, 6]
    dado2 = [1, 2, 3, 4, 5, 6]

    simul = []
    for j in range(simulaciones):
        GrupoUnLanz = []
        for i in range(lanzamientos):
            NumAleatorio1 = random.choice(dado1)
            NumAleatorio2 = random.choice(dado2)
            GrupoUnLanz.append([NumAleatorio1, NumAleatorio2])
        simul.append(GrupoUnLanz)
    return simul

@app.route('/', methods=['GET', 'POST'])
def index():
    global global_acumulador, resultados_globales
    if 'lanzamientos' not in session:
        session['lanzamientos'] = []
    if 'nombre' not in session:
        session['nombre'] = None
    
    if request.method == 'POST':
        if 'ha_lanzado' not in session or not session['ha_lanzado']:
            nombre = request.form['nombre']
            veces = int(request.form['veces'])
            resultados = ListaSimulaciones(veces, 1)[0]
            session['lanzamientos'] = resultados
            global_acumulador += veces
            session['ha_lanzado'] = True
            session['nombre'] = nombre
            resultados_globales.extend(resultados)
    
    return render_template('index.html', lanzamientos=session.get('lanzamientos', []), acumulador=global_acumulador)

@app.route('/probabilidad', methods=['GET', 'POST'])
def probabilidad():
    global global_acumulador, resultados_globales
    probabilidad = None
    grafico_url = None
    numero = None

    if 'lanzamientos' not in session:
        session['lanzamientos'] = []

    if request.method == 'POST':
        if 'numero' in request.form:
            numero = int(request.form['numero'])
            conteo = sum(1 for lanz in session['lanzamientos'] if sum(lanz) == numero)
            probabilidad = conteo / len(session['lanzamientos'])

            # Generar gráfico de barras con curva de densidad
            sumas = [sum(lanz) for lanz in resultados_globales]
            probabilidades = [sum(1 for suma in sumas if suma == i) / len(sumas) for i in range(2, 13)]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=list(range(2, 13)), y=probabilidades, name='Probabilidades', marker_color='blue', opacity=0.6))

            # Calcular la curva de densidad
            if len(sumas) > 0:
                density = gaussian_kde(sumas)
                xs = np.linspace(2, 12, 1000)
                fig.add_trace(go.Scatter(x=xs, y=density(xs), mode='lines', name='Curva de Densidad', line=dict(color='red')))

            # Convertir gráfico a imagen
            img_bytes = pio.to_image(fig, format='png')
            buffer = io.BytesIO(img_bytes)
            img_str = base64.b64encode(buffer.getvalue()).decode()

            grafico_url = f"data:image/png;base64,{img_str}"
        elif 'reset_global' in request.form:
            global_acumulador = 0  # Reinicia el contador global
            resultados_globales = []
            session.clear()
            session['lanzamientos'] = []  # Reinicia también los lanzamientos individuales

            return redirect(url_for('probabilidad'))

    return render_template('probabilidad.html', acumulador=global_acumulador, probabilidad=probabilidad, grafico_url=grafico_url, numero=numero, total_lanzamientos=len(resultados_globales))

@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
