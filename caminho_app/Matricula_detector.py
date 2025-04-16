import cv2
from ultralytics import YOLO
from Ocr import Ocr

class Matricula_detector:
    def __init__(self, modelo_path, tesseract_path=None):
        self.model = YOLO(modelo_path)
        self.ocr = Ocr(tesseract_path)

    def detetar_matricula(self, imagem_path, mostrar=False):
        imagem = cv2.imread(imagem_path)
        resultados = self.model(imagem_path)
        boxes = resultados[0].boxes

        if not boxes:
            print("Nenhuma matrícula detetada.")
            return None

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            recorte = imagem[y1:y2, x1:x2]

            if mostrar:
                cv2.imshow("matrícula: ", recorte)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return self.ocr.processar(recorte)

        return None
    
    
#Run
ocr = Ocr(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
imagem = cv2.imread("imagens/carro1.jpg")
matricula = ocr.processar(imagem)
print("Matrícula final:", matricula)
