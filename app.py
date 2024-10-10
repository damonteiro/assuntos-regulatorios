import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import datetime
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configurações do banco de dados MySQL
mydb = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True
}

# ... (o restante do seu código permanece o mesmo)


def cadastrar_equipamento(nome_equipamento, marca, local_instalado):
    conn = mysql.connector.connect(**mydb)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO equipamento (nome_equipamento, marca, local_instalado) VALUES (%s, %s, %s)", (nome_equipamento, marca, local_instalado))
    conn.commit()
    cursor.close()
    conn.close()

def listar_equipamento():
    conn = mysql.connector.connect(**mydb)
    cursor = conn.cursor()
    cursor.execute("SELECT nome_equipamento FROM equipamento")
    equipamentos = cursor.fetchall()
    cursor.close()
    conn.close()
    return equipamentos

def registrar_temperatura(reg_temp, turno, nome_equipamento):
    try:
        data_registro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = mysql.connector.connect(**mydb)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO temperatura (data_registro, reg_temp, turno, nome_equipamento) VALUES (%s, %s, %s, %s)", 
                       (data_registro, reg_temp, turno, nome_equipamento))
        conn.commit()

        cursor.close()
        conn.close()

        return f"Temperatura registrada para o equipamento {nome_equipamento} em {data_registro}: {reg_temp:.2f}°C (Turno: {turno})"
    except mysql.connector.Error as e:
        return f"Erro ao registrar temperatura: {e}"

@app.route("/", methods=["GET"])
def index():
    mensagem = request.args.get("mensagem", "")
    equipamentos = listar_equipamento()
    return render_template("index.html", mensagem=mensagem, equipamentos=equipamentos)

@app.route("/registrar_temperatura", methods=["POST"])
def registrar_temperatura_rota():
    nome_equipamento = request.form.get("equipamento")
    reg_temp = float(request.form.get("temperatura"))
    turno = request.form.get("turno")
    mensagem = registrar_temperatura(reg_temp, turno, nome_equipamento)
    return redirect(url_for("index", mensagem=mensagem))

@app.route("/cadastrar_equipamento", methods=["POST"])
def cadastrar_equipamento_rota():
    nome_equipamento = request.form.get("nome_equipamento")
    marca = request.form.get("marca")
    local_instalado = request.form.get("local_instalacao")
    
    cadastrar_equipamento(nome_equipamento, marca, local_instalado)
    
    return redirect(url_for("index"))

@app.route("/temperatura", methods=["GET"])
def temperatura():
    equipamentos = listar_equipamento()
    return render_template("temperatura.html", equipamentos=equipamentos)

@app.route("/equipamento", methods=["GET"])
def equipamento():
    return render_template("equipamento.html")

if __name__ == "__main__":
    app.run(debug=True)
