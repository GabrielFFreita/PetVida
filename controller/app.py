import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from flask import Flask, render_template, request, redirect

from model.conexao_model import conexao
from model.cadastro_model import salvar_cadastro
from model.login_model import acessar_login

conectar = conexao
cursor = conectar.cursor()

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, '..', 'view', 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('redeAmigo.html')

@app.route("/", methods=['GET','POST'])
def s_cadastro():
    resultado_cadastro = salvar_cadastro()
    if "sucesso" in resultado_cadastro.lower():
        return redirect('/')
    else:
        return render_template('redeAmigo.html', mensagem_erro=resultado_cadastro)

@app.route("/Login", methods=['POST'])
def a_login():
    resultado_login = acessar_login()
    if "sucesso" in resultado_login.lower():
        return redirect('/')
    else:
        return render_template('redeAmigo.html', mensagem_erro=resultado_login)

@app.route('/admin_page')
def admin_page():
    try:
        print("🔍 Tentando conectar ao banco de dados...")
        
        # ===== BUSCAR ADMINISTRADORES =====
        cursor.execute("SELECT nome_admin, email, senha FROM adm")
        usuario_adm = cursor.fetchall()
        
        print(f"✅ Admins recuperados: {usuario_adm}")
        print(f"📊 Quantidade de admins: {len(usuario_adm)}")
        
        # Converter para dicionários
        usuarios_lista = []
        for usuario in usuario_adm:
            usuarios_lista.append({
                'nome_admin': usuario[0],
                'email': usuario[1],
                'senha': usuario[2]
            })
        
        print(f"📋 Admins formato final: {usuarios_lista}")

        # ===== BUSCAR FUNCIONÁRIOS =====
        cursor.execute("SELECT nome, email, idade, telefone, senha, cargo, status_funcionario FROM funcionario")
        funcionarios = cursor.fetchall()
        
        print(f"✅ Funcionários recuperados: {funcionarios}")
        print(f"📊 Quantidade de funcionários: {len(funcionarios)}")
        
        # Converter para dicionários
        funcionarios_lista = []
        for funcionario in funcionarios:
            funcionarios_lista.append({
                'nome': funcionario[0],
                'email': funcionario[1],
                'idade': funcionario[2],
                'telefone': funcionario[3],
                'senha': funcionario[4],
                'cargo': funcionario[5],
                'status_funcionario': funcionario[6]
            })
        
        print(f"📋 Funcionários formato final: {funcionarios_lista}")
        
        return render_template("pagina_admin.html", usuario_adm=usuarios_lista, funcionarios=funcionarios_lista)
    
    except Exception as e:
        print(f"❌ Erro ao buscar dados: {e}")
        return f"Erro: {e}", 500
        
if __name__ == '__main__':
    app.run(debug=True)