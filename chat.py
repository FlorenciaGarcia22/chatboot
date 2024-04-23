#Algoritmo que  recibe preguntas de los usuarios, detecta la intención de esas preguntas y brinde una respuesta
#Tkinter biblioteca que crea una interfaz en Python

import tkinter as tk
from tkinter import scrolledtext
import re
import random

class ChatBotApp:
    def __init__(self, master):
        self.master = master
        master.title("ChatSapsBot")

        self.chat_history = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.label = tk.Label(master, text="Yo:", font=("Arial", 12))
        self.label.grid(row=1, column=0, padx=10, pady=10)

        self.user_input = tk.Entry(master)
        self.user_input.grid(row=1,column=1, padx=10, pady=10)

        self.button = tk.Button(master, text="Enviar", bg="grey", fg="white", font=("Arial", 12), command=self.send_message)
        self.button.grid(row=2, columnspan=2, padx=10, pady=10)

        self.bot_response("SapsBot: Hola, soy SapsBot estoy programado para brindar informacion sobre el dengue y protocolo de actuacion en caso de sospecha de portar la enfermedad.")

    def send_message(self):
        user_message = self.user_input.get()
        self.bot_response("Yo: " + user_message)
        self.user_input.delete(0, tk.END)
        bot_reply = get_response(user_message)
        self.bot_response("SapsBot: " + bot_reply)

    def bot_response(self, message):
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.see(tk.END)
#Recibe la entrada del usuario user_input
def get_response(user_input):
    #removemos del mje todos los caracteres especiales  con re.split
    #a la entrada la convierte todo en minúscula con lower
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    #revisamos todas las respuestas posible , recibe como entrada el mje y devuelve la respuesta
    response = check_all_messages(split_message)
    return response

#Funcion que calcula la probabilidad
def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty +=1

    percentage = float(message_certainty) / float (len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
        highest_prob = {}

        def response(bot_response, list_of_words, single_response = False, required_words = []):
            nonlocal highest_prob
            highest_prob[bot_response] = message_probability(message, list_of_words, single_response, required_words)

        response('En que te puedo ayudar hoy?', ['hola','ho','ola', 'klk', 'saludos', 'buenas'], single_response = True)
        response('El dengue es una enfermedad causada por un virus que se transmite a través de la picadura de un mosquito llamado Aedes aegypti.', ['que', 'es', 'va', 'vas', 'dengue'], required_words=['que'])
        response('¿El paciente es menor de edad o mayor de edad?', ['cuales','son', 'los', 'sintomas','del','dengue'], required_words=['sintomas'])
        response('los síntomas del dengue en la infancia pueden ser más variables. Algunos solo pueden manifestar un cuadro pseudogripal, mientras que otros pueden presentar sangrados u otras complicaciones.', ['menor','soy', 'el', 'paciente','es','de','edad'], required_words=['menor'])
        response('Los síntomas del dengue en mayores pueden incluir fiebre alta repentina, dolor de cabeza, músculos, articulaciones y huesos, y a veces una erupción rojiza en brazos y piernas. En casos graves, también pueden presentarse náuseas, vómitos, diarrea, dolor abdominal, dificultad para respirar, hemorragias y alteraciones en la presión.', ['mayor','soy', 'el', 'paciente','es','de','edad'], required_words=['mayor'])
        response('El dengue se transmite cuando una persona infectada es picada por un mosquito Aedes aegypti, que luego se convierte en agente transmisor. Los mosquitos pueden contagiar el virus a otras personas cada vez que pican.', ['trasmite','contagia','como','reproduce', 'dengue',], required_words=['trasmite'])
        response('Para prevenir el dengue, es importante evitar la presencia del mosquito Aedes aegypti. Elimina cualquier recipiente que pueda contener agua estancada dentro y fuera de tu casa.', ['prevenir','evitar','como','puedo', 'dengue',], required_words=['prevenir'])
        response('Si sospechas que tienes dengue, consulta a un médico en hospitales o centros de salud públicos o privados.', ['creo', 'tengo', 'porto','que','debo','hacer'], required_words=['tengo'])
        response('¿Es la primera vez que paciente porta la enfermedad?', ['tratamiento', 'cual', 'es','cual', 'tiene'], required_words=['tratamiento'])
        response('Para los pacientes que tienen dengue por primera vez, el tratamiento se enfoca en aliviar los síntomas, como la fiebre y el dolor, y mantener una hidratación adecuada. Sin embargo, en los casos más graves, puede ser necesario hospitalizar al paciente para monitorear su estado y proporcionar tratamientos de apoyo, como líquidos intravenosos.', ['si', 'primera', 'es','vez','la', 'tiene'], required_words=['si'])
        response('Para los pacientes que tienen dengue por segunda vez, existe un riesgo potencialmente mayor de desarrollar una forma más grave de la enfermedad, conocida como dengue grave o dengue hemorrágico. En estos casos, el tratamiento se vuelve más intensivo y puede requerir una intervención médica más agresiva. Además, se debe tener especial cuidado en la monitorización de la evolución de la enfermedad para detectar cualquier signo de complicaciones de manera temprana.', ['no', 'primera', 'es','vez','la', 'tiene'], required_words=['no'])
        response('El período de incubación del dengue es de 8 a 10 días, y la enfermedad suele durar entre 10 y 15 días.', ['dura', 'duracion', 'tiempo','cuanto','dengue', 'enfermedad'], required_words=['dura'])
        response('Si te pica un mosquito, presta atención a cualquier síntoma y consulta a un médico si es necesario.', ['picadura', 'hacer', 'de','mosquito','dengue'], required_words=['picadura'])
        response('De nada! Adios', ['gracias','muchas gracias', 'adios'], single_response=True)

        best_match = max(highest_prob, key=highest_prob.get)
        #print(highest_prob)

        return unknown() if highest_prob[best_match] < 1 else best_match

def unknown():
    response = ['intenta escribiendo de otra forma','puedes decirlo de nuevo?', 'No estoy seguro de lo que quieres'][random.randrange(3)]
    return response

root = tk.Tk()
app = ChatBotApp(root)
root.mainloop()
