# Faculdade 
    Cesar School

# Período
    2025.1

# Disciplina
    Projeto 1

# Professor
    Humberto Caetano

# Equipe
    Artur Cavalcanti
    Eduardo Henrique Ferreira Fonseca Barbosa
    Evandro José Rodrigues Torres Zacarias
    Gabriel de Medeiros Almeida
    Maria Clara Miranda
    Mauro Sérgio Rezende da Silva
    Silvio Barros Tenório

# Projeto
    App de Denúncia de Bullying Anônima

    - Módulo Denunciante
    - Módulo Gerencial

# Comandos
    - Cria ambiente virtual
        python -m venv venv

    - Ativar ambiente virtual
        * Linux/Mac:
            source venv/bin/activate
        * Windows:
            venv/Scripts/activate

    - Lista os pacotes instalados
        pip freeze

    - Gerar arquivo requirements.txt
        pip freeze > requirements.txt

    - Recuperar venv com requirements.txt
        pip install -r ./requirements.txt
    
    - Atualizar o pip
        python.exe -m pip install --upgrade pip

    - Instalar o Flet
        pip install flet
    
    - Instalar o BCrypt:
        pip install bcrypt

    - BCrypt
        Melhor para: Aplicações que exigem segurança máxima.
        Vantagens:
            - Algoritmo consagrado: Especificamente projetado para senhas (usa salt automático).
            - Adaptável: O "fator de trabalho" (rounds) pode ser aumentado conforme hardware evolui.
            - Resistente a GPU/ASIC: Mais lento para ataques de força bruta.
