from config import ocrp

def paddle_ocr(plate_img):
    result = ocrp.ocr(plate_img, cls=False)
    
    text = ''
    for line in result:
        if line is not None:
            for word in line:
                text += word[1][0]
            text += '\n'
    
    return text.strip().replace(" ","")