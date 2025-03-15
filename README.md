# Reconhecimento Facial com Python  // apenas o código

Este projeto utiliza reconhecimento facial para identificar pessoas através de uma webcam e registrar suas presenças em um arquivo Excel.

## Funcionalidades

* Reconhecimento facial em tempo real utilizando a webcam.
* Identificação de pessoas com base em uma base de dados de rostos conhecidos.
* Registro de presenças em um arquivo Excel, incluindo nome, data e hora.
* Captura de imagens de rostos desconhecidos e armazenamento em uma pasta separada.

## Pré-requisitos

* Python 3.x
* Bibliotecas Python:
    * OpenCV (`cv2`)
    * face_recognition
    * pandas
    * openpyxl (para trabalhar com arquivos Excel)

Você pode instalar as bibliotecas utilizando o pip:

```bash
pip install opencv-python face_recognition pandas openpyxl
