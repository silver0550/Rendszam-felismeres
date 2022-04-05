import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def text_filter(text):
    result = ''
    for letter in text:
        if letter == '=':
            result += '-'

        if (letter >='A' and letter <= 'Z') or (letter >='0' and letter <= '9') or letter == '-':
            result += letter

    return result

def get_text(picture, custom_config=r'--oem 3 --psm 10'):
    text = tess.image_to_string(picture, lang='eng', config=custom_config).rstrip()
    text = text_filter(text)
    return text




if __name__ == "__main__":
    res = text_filter('PBC=781')
    print(res)


