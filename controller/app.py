import sys
import os

print(sys.path)



from flask import Flask, render_template, request, redirect


from model.conexao_model import conexao
from model.cadastro_model import salvar_cadastro
from model.login_model import acessar_login


conectar = conexao





current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'view', 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    
    return render_template('redeAmigo.html')

@app.route("/", methods=['POST'])
def s_cadastro():
    
    resultado_cadastro = salvar_cadastro()
 
    
    if "sucesso" in resultado_cadastro.lower():
        

        return redirect(('/'))
        
    else:
        
        return render_template('redeAmigo.html', mensagem_erro=resultado_cadastro)

@app.route("/Login", methods=['POST'])
def a_login():
    resultado_login = acessar_login()
    
    
    if "sucesso" in resultado_login.lower():
        
        
        return redirect(('/')) 
        
    else:
        
        return render_template('redeAmigo.html', mensagem_erro=resultado_login)
    

if __name__ == '__main__':
    
    app.run(debug=True)