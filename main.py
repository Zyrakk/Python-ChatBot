import json
from difflib import get_close_matches

def load_data(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        datos: dict = json.load(file)
    return datos

def save_data(file_path: str, datos: dict):
    with open(file_path, 'w') as file:
        json.dump(datos, file, indent=2)

def find_data(pregunta_usuario: str, preguntas: list[str]) -> str | None:
    coincidencias: list = get_close_matches(pregunta_usuario, preguntas, n=1, cutoff=0.6)
    return coincidencias[0] if coincidencias else None

def get_answer(pregunta: str, database: dict) -> str | None:
    for p in database["preguntas"]:
        if p["pregunta"] == pregunta:
            return p["respuesta"]
        
def chatbot():
    database: dict = load_data('database.json')
    
    while True:
        user_input: str = input('Tu:')
        
        if user_input.lower() == 'salir':
            break
        
        mejor_resultado: str | None = find_data(user_input, [p["pregunta"] for p in database["preguntas"]])
        
        if mejor_resultado:
            respuesta: str = get_answer(mejor_resultado, database)
            print(f'Bot: {respuesta}')
        else:
            print('Bot: No conozco la respuesta a lo que has dicho. ¿Me dices la respuesta?')
            nueva_respuesta: str = input('Introduce la respuesta o escribe "salir" para salir: ')
            
            if nueva_respuesta.lower() != 'salir':
                database["preguntas"].append({"pregunta": user_input, "respuesta": nueva_respuesta})
                save_data('database.json', database)
                print('Bot: ¡Gracias! He aprendido una nueva respuesta')
                
                
if __name__ == '__main__':
    chatbot()
