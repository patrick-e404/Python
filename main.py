import cv2
import face_recognition
import pandas as pd
from datetime import datetime
import os

webcam = cv2.VideoCapture(0)

nome_arquivo = 'registro_rostos.xlsx'
pasta_base_rostos = 'base_de_dados_rostos'
pasta_desconhecidos = 'desconhecidos'
os.makedirs(pasta_desconhecidos, exist_ok=True)

rostos_conhecidos = []
nomes_conhecidos = []

for nome_pessoa in os.listdir(pasta_base_rostos):
    caminho_pessoa = os.path.join(pasta_base_rostos, nome_pessoa)
    if os.path.isdir(caminho_pessoa):
        for arquivo_imagem in os.listdir(caminho_pessoa):
            caminho_imagem = os.path.join(caminho_pessoa, arquivo_imagem)
            imagem = face_recognition.load_image_file(caminho_imagem)
            try:
                encoding = face_recognition.face_encodings(imagem)[0]
                rostos_conhecidos.append(encoding)
                nomes_conhecidos.append(nome_pessoa)
            except IndexError:
                print(f"Rosto não detectado em {arquivo_imagem}, ignorando.")

if not os.path.exists(nome_arquivo):
    df = pd.DataFrame(columns=['Nome', 'Data', 'Hora'])
    df.to_excel(nome_arquivo, index=False)

ultimo_nome_registrado = None

while webcam.isOpened():
    validacao, frame = webcam.read()
    if not validacao:
        break

    imagem = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locais_rostos = face_recognition.face_locations(imagem)
    encodings_rostos = face_recognition.face_encodings(imagem, locais_rostos)

    agora = datetime.now()
    timestamp = agora.strftime("%Y%m%d_%H%M%S")

    nome_detectado = "Desconhecido"

    for encoding in encodings_rostos:
        resultados = face_recognition.compare_faces(rostos_conhecidos, encoding)
        if True in resultados:
            indice = resultados.index(True)
            nome_detectado = nomes_conhecidos[indice]
        else:
            caminho_arquivo = os.path.join(pasta_desconhecidos, f"desconhecido_{timestamp}.jpg")
            cv2.imwrite(caminho_arquivo, frame)

    if nome_detectado != ultimo_nome_registrado:
        nova_entrada = pd.DataFrame([{
            'Nome': nome_detectado,
            'Data': agora.strftime("%Y-%m-%d"),
            'Hora': agora.strftime("%H:%M:%S")
        }])
        df = pd.read_excel(nome_arquivo)
        df = pd.concat([df, nova_entrada], ignore_index=True)
        df.to_excel(nome_arquivo, index=False)
        ultimo_nome_registrado = nome_detectado

    for (top, right, bottom, left), nome in zip(locais_rostos, [nome_detectado] * len(locais_rostos)):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, nome, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(5) == 27:
        break

webcam.release()
cv2.destroyAllWindows()