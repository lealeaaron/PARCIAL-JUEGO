import threading
import pygame
import random
import sys
import json
import csv
import re
import random
######################################  FUNCIONES  ######################################
def pantalla_de_inicio():
    x = 0
    y = 0
    texto_inicio = "Presione Enter para comenzar"
    texto_superficie = fuente_texto.render(texto_inicio, True, BLANCO)
    VENTANA.blit(texto_superficie, (x + 263, y + 350))
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return 

########################################################



def contar_tiempo():
    global tiempo
    while tiempo > 0:
        tiempo -= 1
        pygame.time.delay(1000)
    if respuesta is None:
        print("¡Tiempo agotado!")
        resultado, puntaje = False, 0



########################################################
def datos_guardados(registro):
    VENTANA.fill(NEGRO)
    texto_indicativo = "Por Favor, escriba su nombre en la consola"
    texto_indicativo_presentar = fuente_texto.render(texto_indicativo, True, BLANCO)
    VENTANA.blit(texto_indicativo_presentar, (x + 210, y +350))
    pygame.display.update()
    if registro:
        nombre = input("Por favor, ingrese su nombre: ")  # Solicitar el nombre al usuario
        if nombre:
            with open('puntajes.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                data = [f'Nombre: {nombre}', f'Preguntas Contestadas: {registro[-1][0]}', f'Plata Ganada: {registro[-1][1]}']
                writer.writerow(data)  # Agregar el nombre y los datos más recientes
            print("Datos guardados en puntajes.csv")
            print("Gracias por jugar")
            sys.exit()
        else:
            print("No se ingresó un nombre.")
    else:
        print("No hay datos para guardar.")
        print("Gracias por jugar")
        sys.exit()
    




########################################################



def verificar_respuesta(pregunta,respuesta,puntaje):
    if respuesta == pregunta["respuesta_correcta"] :
        puntaje += int(pregunta['valor'])
        resultado = True 
    else:
        resultado = False
    return resultado,puntaje



########################################################



def votos_del_publico(pregunta, respuesta, puntaje):

    for i in range(4):
        porcentaje = random.randint(1,100)
        if i == 0:
            x, y = 25, 730
        elif i == 1:
            x, y = 25, 770
        elif i == 2:
            x, y = 475, 730
        elif i == 3:
            x, y = 475, 770

        texto_porcentaje = fuente_texto.render(f"{porcentaje}:", False, BLANCO)
        VENTANA.blit(texto_porcentaje, (x, y))
        pygame.display.update()

    respuesta = None
    while respuesta is None:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1 or evento.key == pygame.K_KP_1:
                    respuesta = "a"
                elif evento.key == pygame.K_2 or evento.key == pygame.K_KP_2:
                    respuesta = "b"
                elif evento.key == pygame.K_3 or evento.key == pygame.K_KP_3:
                    respuesta = "c"
                elif evento.key == pygame.K_4 or evento.key == pygame.K_KP_4:
                    respuesta = "d"
                elif evento.key == pygame.K_5 or evento.key == pygame.K_KP_5:
                    respuesta = "publico"
                elif evento.key == pygame.K_6 or evento.key == pygame.K_KP_6:
                    respuesta = "llamada"
                elif evento.key == pygame.K_7 or evento.key == pygame.K_KP_7:
                    respuesta = "50-50"
    
    return verificar_respuesta(pregunta, respuesta, puntaje)



########################################################
def buscar_preguntas(lista, valor:int, preguntas_utilizadas):
    lista_pregunta = []

    for elemento in lista:
        if elemento["valor"] == valor and elemento not in preguntas_utilizadas:
            lista_pregunta.append(elemento)

    numero_random = random.randint(0, len(lista_pregunta) - 1)
    pregunta_seleccionada = lista_pregunta[numero_random]
    preguntas_utilizadas.append(pregunta_seleccionada)

    return pregunta_seleccionada


########################################################
def mostrar_preguntas_y_datos(etapa,ganancias):
    x = 0
    y = 0
    escalon = 0
    VENTANA.blit(fondo_asignado, (0, 0))
    pygame.draw.rect(VENTANA, NEGRO, pygame.Rect(int(x), 725, 800, 75))
    pygame.draw.rect(VENTANA, BLANCO, pygame.Rect(int(x), 75, 800, 5))
    pygame.draw.rect(VENTANA, NEGRO, pygame.Rect(int(x), 80, 800, 95))
    pygame.draw.rect(VENTANA, NEGRO, pygame.Rect(250, 700, 300, 25))
    pygame.draw.rect(VENTANA, NEGRO, pygame.Rect(int(x), int(y), 800, 75))
    pygame.draw.rect(VENTANA, BLANCO, pygame.Rect(600, int(y), 5, 75))
    texto_pregunta = fuente_texto.render(pregunta["pregunta"], False, BLANCO)
    premio = fuente_chica.render(ganancias, False, BLANCO)
    etapa= fuente_chica.render(etapa, False, BLANCO)
    el_5 = "pedir voto del publico: 5"
    el_6 = "pedir una pista: 6"
    el_7 = "quitar 2 opciones: 7"
    el_5_presentar = fuente_chica.render(el_5, False, BLANCO)
    el_6_presentar = fuente_chica.render(el_6, False, BLANCO)
    el_7_presentar = fuente_chica.render(el_7, False, BLANCO)
    VENTANA.blit(el_5_presentar, (25 , 90))
    VENTANA.blit(el_6_presentar, (25 , 120))
    VENTANA.blit(el_7_presentar, (25 , 150))
    VENTANA.blit(etapa, (x + 615, 25))
    VENTANA.blit(premio, (x + 265, 700))
    VENTANA.blit(texto_pregunta, (x + 20, y +20))
    y += 50
    for opcion in pregunta["opciones"]:
        x += 450
        escalon += 1
        if escalon == 1:
            # Reemplaza "a)" por "1)"
            opcion = re.sub(r'^[aA]\)', '1)', opcion)
            texto_opcion = fuente_texto.render(opcion, False, BLANCO)
            VENTANA.blit(texto_opcion, (75, y + 680))
        elif escalon == 2:
            # Reemplaza "b)" por "2)"
            opcion = re.sub(r'^[bB]\)', '2)', opcion)
            texto_opcion = fuente_texto.render(opcion, False, BLANCO)
            VENTANA.blit(texto_opcion, (75, y + 720))
        elif escalon == 3:
            # Reemplaza "c)" por "3)"
            opcion = re.sub(r'^[cC]\)', '3)', opcion)
            texto_opcion = fuente_texto.render(opcion, False, BLANCO)
            VENTANA.blit(texto_opcion, (525, y + 680))
        elif escalon == 4:
            # Reemplaza "d)" por "4)"
            opcion = re.sub(r'^[dD]\)', '4)', opcion)
            texto_opcion = fuente_texto.render(opcion, False, BLANCO)
            VENTANA.blit(texto_opcion, (525, y + 720))

########################################################



def mostrar_pista(pista):
    x = 0
    y = 0
    pista_texto = fuente_texto.render(pista, False, BLANCO)
    pygame.draw.rect(VENTANA, NEGRO, pygame.Rect(250, 80, 550, 70))
    VENTANA.blit(pista_texto, (500, 100))
    


#######################################################



def eliminar_dos_opciones_incorrectas(pregunta):
    opciones = pregunta["opciones"]
    respuesta_correcta = pregunta["respuesta_correcta"]
    
    # Filtrar las opciones incorrectas (diferentes de la respuesta correcta)
    opciones_incorrectas = [opcion for opcion in opciones if not opcion.startswith(respuesta_correcta)]

    # Elegir dos opciones incorrectas aleatorias para eliminar
    opciones_a_eliminar = random.sample(opciones_incorrectas, 2)
    
    # Eliminar las opciones seleccionadas
    opciones = [opcion for opcion in opciones if opcion not in opciones_a_eliminar]
    
    # Actualizar las opciones en la pregunta
    pregunta["opciones"] = opciones
    pygame.draw.rect(VENTANA, NEGRO, pygame.Rect(int(x), 725, 800, 75))
    mostrar_preguntas_y_datos(etapa, ganancias)
    pygame.display.update()
    



########################################################
def mostrar_perdiste(registro):
    x = 0
    y = 0
    texto_inicio = "Presione Enter para volver a intentar"
    texto_perdiste = "Game Over"
    texto_guardar = "presione 5 para guardar el puntaje"
    texto_perdiste_presentar = fuente_texto.render(texto_perdiste, True, BLANCO)
    texto_inicio_presentar = fuente_texto.render(texto_inicio, True, BLANCO)
    texto_guardar_presentar = fuente_texto.render(texto_guardar, True, BLANCO)
    VENTANA.blit(texto_guardar_presentar, (x + 50, y + 100))
    VENTANA.blit(texto_inicio_presentar, (x + 50, y + 50))
    VENTANA.blit(texto_perdiste_presentar, (x + 350, y +350))
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return # Sale de la función al presionar Enter
                elif evento.key == pygame.K_5 or evento.key == pygame.K_KP_5:
                    datos_guardados(registro)




######################################  MAIN  ##############################################
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AZUL_CLARO = (0,150,255)
color_cuadrado = BLANCO
ANCHO_VENTANA = 800
ALTO_VENTANA = 800


pygame.init()
fuente_texto = pygame.font.SysFont("Arial",20)
fuente_chica = pygame.font.SysFont("Arial",18)
VENTANA = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("Preguntas Parcial")
lista_valores = [100, 200,300,500,1000]


with open("preguntas.json", "r", encoding="utf-8") as archivo_json:
    lista_preguntas = json.load(archivo_json)


clock = pygame.time.Clock()
tiempo = 30
flag = True
llamada = False
comenzar = False
mostrar_pantalla_inicio = True
pase_a_datos_guardados = False
perdiste = False
veri_o_voto = False
fondo_asignado = pygame.image.load("billetes.jpg")
fondo_asignado = pygame.transform.scale(fondo_asignado, (900,900))
puntaje = 0
contestadas = 0
rango = 100
plata = 0
etapa = "Etapa: Dolar"
registro = []
preguntas_utilizadas = []


while flag:
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag = False
        x = 0
        y = 0
        VENTANA.fill(NEGRO)

        if mostrar_pantalla_inicio == True and perdiste == False:
            pantalla_de_inicio()
            mostrar_pantalla_inicio = False
        elif perdiste == True:
            perdiste = mostrar_perdiste(registro)

        #buscar pregunta y sus opciones designadas
        if not mostrar_pantalla_inicio:
            pregunta = buscar_preguntas(lista_preguntas, rango, preguntas_utilizadas)
            opciones = "\n"
            opciones = opciones.join(pregunta["opciones"])
            respuesta = None
        
        tiempo = 30
        timer_thread = threading.Thread(target=contar_tiempo)
        timer_thread.start()

        plata = int(plata)
        ganancias = f"Premio: {str(plata)}$"
        llamada = mostrar_preguntas_y_datos(etapa,ganancias)
        
        pygame.display.update()
        
        # Bucle para esperar la respuesta del usuario
        respuesta = None
        while respuesta is None and tiempo > 0:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1 or evento.key == pygame.K_KP_1:
                        respuesta = "a"
                    elif evento.key == pygame.K_2 or evento.key == pygame.K_KP_2:
                        respuesta = "b"
                    elif evento.key == pygame.K_3 or evento.key == pygame.K_KP_3:
                        respuesta = "c"
                    elif evento.key == pygame.K_4 or evento.key == pygame.K_KP_4:
                        respuesta = "d"
                    elif evento.key == pygame.K_5 or evento.key == pygame.K_KP_5:
                        respuesta = "publico"
                    elif evento.key == pygame.K_6 or evento.key == pygame.K_KP_6:
                        if pregunta["pista"]:
                            mostrar_pista(pregunta["pista"])  # Mostrar la pista
                            pygame.display.update()
                        else:
                            respuesta = "incorrecta"
                    elif evento.key == pygame.K_7 or evento.key == pygame.K_KP_7:
                        eliminar_dos_opciones_incorrectas(pregunta) 
                        


        if respuesta == "publico":
            resultado, puntaje = votos_del_publico(pregunta, respuesta, puntaje)
            veri_o_voto = True
        

        
        if veri_o_voto == False:
            resultado, puntaje = verificar_respuesta(pregunta, respuesta, puntaje)
        veri_o_voto = False

        
        if resultado:
            print(f"Puntuación: {str(puntaje)}")
            contestadas += 1
            if plata == 0:
                plata += 100 
            else:
                plata = plata + (plata * 0.50)

            registro.append((contestadas, int(plata)))        
            if len(registro) > 1:
                registro.pop(0)
        else:
            print("Game over")
            perdiste = True
            puntaje = 0
            plata = 0
            preguntas_utilizadas = []
            contestadas = 0
            rango = 100
            fondo_asignado = pygame.image.load("billetes.jpg")
            fondo_asignado = pygame.transform.scale(fondo_asignado, (ANCHO_VENTANA,ALTO_VENTANA))
            etapa = "Etapa: Dolar"
        
        if contestadas == 5:
            rango = 200
            fondo_asignado = pygame.image.load("rango bronze.jpg")
            fondo_asignado = pygame.transform.scale(fondo_asignado, (1000,800))
            etapa = "Etapa: Bronze"
        if contestadas == 10:
            rango = 300
            fondo_asignado = pygame.image.load("plata.jpg")
            fondo_asignado = pygame.transform.scale(fondo_asignado, (1200,ALTO_VENTANA))
            etapa = "Etapa: Plata"
        if contestadas == 15:
            rango = 500
            fondo_asignado = pygame.image.load("oro.jpg")
            fondo_asignado = pygame.transform.scale(fondo_asignado, (ANCHO_VENTANA,ALTO_VENTANA))
            etapa = "Etapa: Oro"
        if contestadas == 20:
            rango = 1000
            fondo_asignado = pygame.image.load("diamante.jpg")
            fondo_asignado = pygame.transform.scale(fondo_asignado, (ANCHO_VENTANA,ALTO_VENTANA))
            etapa = "Etapa: Diamante"
        



        # Espera a que el usuario presione una tecla antes de continuar


    pygame.quit()
sys.exit()





#El participante contará con 30 segundos para contestar cada pregunta.
#En caso de una respuesta incorrecta o en caso de quedarse sin tiempo, el juego termina.




