from flask import request, jsonify
from model.conexao_model import conexao

def acessar_login():
    email = request.form.get('Email')
    senha = request.form.get('Senha')

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    try:
        cursor = conexao.cursor(dictionary=True)
        sql_c = "SELECT email, senha FROM Usuario WHERE email = %s AND senha = %s"
        cursor.execute(sql_c, (email, senha))
        resultado = cursor.fetchone()  # pega o primeiro registro, se existir

        if resultado:
            return jsonify({"mensagem": "Login realizado com sucesso"}), 200
        else:
            return jsonify({"erro": "Email ou senha incorretos"}), 401

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    finally:
        cursor.close()
