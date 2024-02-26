import os

def get_user_home_folder():
    if os.name == 'posix':  # Verifica se é um sistema tipo Unix (Linux, macOS, etc.)
        return os.getenv('HOME')
    elif os.name == 'nt':  # Verifica se é um sistema Windows
        return os.getenv('USERPROFILE')
    else:
        raise OSError('Sistema operacional não suportado')

# Exemplo de uso
user_home_folder = get_user_home_folder()
print(f'A pasta do usuário é: {user_home_folder}')