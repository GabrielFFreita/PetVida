from flask import request, render_template
from model.conexao_model import conexao 

def salvar_cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    idade = request.form.get('idade') 
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')
    tipo = request.form.get('tipoUsuario')
    cargo = request.form.get('cargo')

    cursor = None
    resultado = "Cadastro realizado com sucesso!"

    try:
        cursor = conexao.cursor(dictionary=True)

        # Verifica se já existe usuário ou funcionário com o mesmo nome
        sql_u = """
           SELECT email FROM usuario WHERE nome = %s
            UNION
            SELECT email FROM funcionario WHERE nome = %s

        """
        cursor.execute(sql_u, (email, email))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return render_template('redeAmigo.html', mensagem_erro="Erro no cadastro: email do usuário já existe.")

        # Valores para inserção
        vlrc = (nome, idade, telefone, email, senha) 
        vlrf = (nome, email, idade, telefone, senha, cargo) 

        if tipo == "cliente":
            sql_c = "INSERT INTO usuario (nome, idade, telefone, email, senha) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_c, vlrc)

        elif tipo == "funcionario":
            sql_f = "INSERT INTO funcionario (nome, email, idade, telefone, senha, cargo) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_f, vlrf)

        else:
            raise ValueError("Erro no cadastro: Tipo de usuário ('tipo') inválido.")

        conexao.commit()

    except Exception as e:
        if conexao:
            conexao.rollback()
        print(f"Erro no cadastro: {e}")
        resultado = "Erro ao cadastrar. Tente novamente." 

    finally:
        if cursor:
            cursor.close()

    return resultado
