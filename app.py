import psycopg2
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

def get_connection():
    try:
        return psycopg2.connect(os.environ.get("DB_URL"))
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_connection()
    if not conn: return jsonify({"erro": "Sem conexão"}), 500
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.UsuarioID, u.Nome, u.Saldo, 
            COALESCE((SELECT i.Tipo FROM Inscricoes i WHERE i.UsuarioID = u.UsuarioID LIMIT 1), 'NORMAL') as Tipo,
            (SELECT COUNT(*) FROM Inscricoes WHERE UsuarioID = u.UsuarioID AND Status = 'Confirmada') as Presencas
            FROM Usuarios u ORDER BY u.UsuarioID;
        """)
        rows = cur.fetchall()
        usuarios = [{"id": r[0], "nome": r[1], "saldo": float(r[2]), "tipo": r[3], "presencas": r[4]} for r in rows]
        return jsonify(usuarios)
    finally:
        if conn: conn.close()


@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    prioridade = dados.get('prioridade', 3)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Usuarios (Nome, Email, Prioridade, Saldo) VALUES (%s, %s, %s, 100.00) RETURNING UsuarioID;", (nome, email, prioridade))
        novo_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"status": "sucesso", "message": f"Usuário {nome} criado!", "id": novo_id}), 201
    finally:
        if conn: conn.close()


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Usuarios WHERE UsuarioID = %s", (id,))
        conn.commit()
        return jsonify({"status": "sucesso", "message": "Usuário removido!"})
    finally:
        if conn: conn.close()


@app.route('/distribuir', methods=['POST'])
def distribuir():
    conn = get_connection()
    try:
        cur = conn.cursor()
        script = """
        DO $$
        DECLARE
            reg RECORD;
        BEGIN
            FOR reg IN SELECT i.InscricaoID, i.UsuarioID, i.ValorPago FROM Inscricoes i WHERE i.Status = 'Confirmada' LOOP
                UPDATE Usuarios SET Saldo = Saldo + (reg.ValorPago * 0.10) WHERE UsuarioID = reg.UsuarioID;
                INSERT INTO Log_Auditoria (InscricaoID, Motivo) VALUES (reg.InscricaoID, 'CASHBACK APLICADO');
            END LOOP;
        END $$;
        """
        cur.execute(script)
        conn.commit()
        return jsonify({"status": "sucesso", "message": "Cashback distribuído!"})
    finally:
        if conn: conn.close()


@app.route('/resetar', methods=['POST'])
def resetar_sistema():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            DO $$ BEGIN
                TRUNCATE TABLE Log_Auditoria RESTART IDENTITY;
                UPDATE Usuarios SET Saldo = 100.00;
            END $$;
        """)
        conn.commit()
        return jsonify({"status": "sucesso", "message": "Sistema resetado!"})
    finally:
        if conn: conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)