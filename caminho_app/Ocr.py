import cv2
import pytesseract
from ultralytics import YOLO

def detectar_matricula_yolo(imagem_path):
    imagem = cv2.imread(imagem_path)
    model = YOLO("path_to_model")
    results = model(imagem_path)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            recorte = imagem[y1:y2, x1:x2]
            
            # OCR
            texto = pytesseract.image_to_string(recorte, config='--psm 8')
            return texto.strip()
    
    return "Matrícula não detetada"

# Exemplo de uso
imagem = "carro1.jpg"
matricula = detectar_matricula_yolo(imagem)
print("Matrícula detetada:", matricula)
