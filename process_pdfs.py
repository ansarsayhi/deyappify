import requests
from io import BytesIO
from pdfminer.high_level import extract_text
from get_links import sections_list


def get_text():

    texts = []
    for session in sections_list:
        for pdf in session[1]:
            response = requests.get(pdf)
            response.raise_for_status()
            pdf_text = extract_text(BytesIO(response.content))
            texts.append(pdf_text)
    return texts


if __name__ == "__main__":
    texts = get_text()

