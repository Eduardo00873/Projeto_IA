import cv2
import pytesseract
import re
from ultralytics import YOLO

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
model = YOLO("license_plate_detector.pt")

correcao_ocr = {
    "O": "0", "I": "1", "L": "1", "B": "8", "S": "5", "Z": "2", "Q": "0", "G": "6", "D": "0",
    "5": "6"
}

def remover_banda_azul_esquerda(imagem):
    altura, largura = imagem.shape[:2]
    corte = int(largura * 0.11)
    return imagem[:, corte:] 

def corrigir_texto(texto):
    return "".join([correcao_ocr.get(c.upper(), c.upper()) for c in texto])

def extrair_texto_matricula(recorte):
    recorte = remover_banda_azul_esquerda(recorte)
    cinza = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contraste = clahe.apply(cinza)
    ampliada = cv2.resize(contraste, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, binarizada = cv2.threshold(ampliada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    inversa = cv2.bitwise_not(binarizada)

    config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    texto = pytesseract.image_to_string(inversa, config=config)
    return corrigir_texto(texto.strip())

def validar_matricula(texto):
    texto = texto.replace(" ", "").replace("-", "").replace("\n", "")
    texto = texto[:6]

    padroes = [
        r"[A-Z]{2}\d{2}[A-Z]{2}",
        r"\d{2}[A-Z]{2}\d{2}",
        r"[A-Z]{2}\d{4}",
        r"\d{4}[A-Z]{2}",
        r"\d{2}\d{2}[A-Z]{2}",
    ]
    for padrao in padroes:
        if re.fullmatch(padrao, texto):
            return texto
    return texto


def formatar_matricula(texto):
    if len(texto) == 6:
        if texto[:2].isalpha() and texto[2:4].isdigit() and texto[4:].isalpha():
            return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"
        elif texto[:2].isdigit() and texto[2:4].isalpha() and texto[4:].isdigit():
            return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"
        elif texto[:4].isdigit() and texto[4:].isalpha():
            return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"
        elif texto[:2].isalpha() and texto[2:].isdigit():
            return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"
    return texto

def detetar_matricula(imagem_path):
    imagem = cv2.imread(imagem_path)
    resultados = model(imagem_path)
    boxes = resultados[0].boxes

    if not boxes:
        print("Nenhuma matrícula detetada.")
        return

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        recorte = imagem[y1:y2, x1:x2]

        texto_ocr = extrair_texto_matricula(recorte)
        texto_validado = validar_matricula(texto_ocr)
        matricula_final = formatar_matricula(texto_validado)

        print(f"Matrícula detetada: {matricula_final}")
        return matricula_final

    print("Erro")
    return



# --- Teste com imagem ---

if __name__ == "__main__":
    caminho_imagem = "imagens/carro2.jpg"  # <- atualiza com o caminho real da tua imagem
    detetar_matricula(caminho_imagem)
