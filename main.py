# Este es el archivo que se deeria de ejecutar para ejecutar todo el programa
# 1. Importas la clase desde el otro archivo
from usuario import Usuario 

# 2. Defines la función principal
def main():
    print("Iniciando el programa...")
    
    # 3. Usas las clases del otro archivo
    persona = Usuario("Carlos")
    persona.saludar()

# 4. El disparador obligatorio de Python
if __name__ == '__main__':
    main()
