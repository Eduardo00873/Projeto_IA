import cv2
import pytesseract
import re
from ultralytics import YOLO

class Ocr:
    correcao_ocr = {
        "O": "0", "I": "1", "L": "1", "B": "8", "S": "5", "Z": "2", "Q": "0", "G": "6", "D": "0",
        "5": "6"
    }

    def __init__(self, tesseract_path=None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def remover_banda_azul_esquerda(self, imagem):
        altura, largura = imagem.shape[:2]
        corte = int(largura * 0.11)
        return imagem[:, corte:]

    def corrigir_texto(self, texto):
        return "".join([self.correcao_ocr.get(c.upper(), c.upper()) for c in texto])

    def extrair_texto(self, recorte):
        recorte = self.remover_banda_azul_esquerda(recorte)
        cinza = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        contraste = clahe.apply(cinza)
        ampliada = cv2.resize(contraste, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, binarizada = cv2.threshold(ampliada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        inversa = cv2.bitwise_not(binarizada)

        config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        texto = pytesseract.image_to_string(inversa, config=config)
        return self.corrigir_texto(texto.strip())

    def validar_matricula(self, texto):
        texto = texto.replace(" ", "").replace("-", "").replace("\n", "")[:6]
        padroes = [
            r"[A-Z]{2}\d{2}[A-Z]{2}", r"\d{2}[A-Z]{2}\d{2}", r"[A-Z]{2}\d{4}",
            r"\d{4}[A-Z]{2}", r"\d{2}\d{2}[A-Z]{2}"
        ]
        for padrao in padroes:
            if re.fullmatch(padrao, texto):
                return texto
        return texto

    def formatar_matricula(self, texto):
        if len(texto) == 6:
            return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"
        return texto

    def processar(self, recorte):
        texto_ocr = self.extrair_texto(recorte)
        texto_validado = self.validar_matricula(texto_ocr)
        return self.formatar_matricula(texto_validado)


class Matricula_detector:
    def __init__(self, modelo_path, tesseract_path=None):
        print(f"Path do modelo: {modelo_path}")
        self.model = YOLO(modelo_path)
        self.ocr = Ocr(tesseract_path)

    def detetar_matricula(self, imagem_path, mostrar=False):
        imagem = cv2.imread(imagem_path)
        resultados = self.model(imagem_path)
        boxes = resultados[0].boxes

        if not boxes:
            return None

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            recorte = imagem[y1:y2, x1:x2]
            if mostrar:
                cv2.imshow("Matrícula Detetada", recorte)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return self.ocr.processar(recorte)

        return None
