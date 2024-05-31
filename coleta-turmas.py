import io
import re
import requests
import PyPDF2
import pandas as pd
from datetime import datetime


# Gera um iterador para as turmas
def classes_generator(classes_list: list):
    for element in classes_list:
        yield element


# Gera um iterador para os membros
def members_generator(members_dataframe: pd.DataFrame):
    for index, row in members_dataframe.iterrows():
        yield row["RA"], row["Nome completo"]


# Pega o conteúdo do PDF
def get_content(url):
    content = []
    try:
        web_page = requests.get(url)
        file = io.BytesIO(web_page.content)
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            content.append(page.extract_text())
        return content

    except:
        return False


# Transforma o conteúdo do PDF em linhas
def make_lines(pages):
    for i in range(0, len(pages)):
        pages[i] = pages[i].split("\n")

    lines = []
    for page in pages:
        for line in page:
            lines.append(line.lstrip())

    return lines


# Seleciona as linhas que contém as turmas
def select_content(lines, ra_list):
    classes = []

    for line in classes_generator(lines):
        verified_line = verify_line(line)
        if verified_line:
            classes.append(verified_line) if verified_line["RA"] in ra_list else None

    return classes


# Verifica se a linha contém uma turma e retorna um dicionário com as informações
def verify_line(line):
    def cut_line(ra, code, line):
        position = len(ra) + len(code) + 2
        return line[position::]

    ra_pattern1 = r"11[0-9]{9}"
    ra_pattern2 = r"[0-9]{8}"
    code_pattern = r"[A-Z0-9]{7}[0-9]{2,3}-[0-9]{2}[A-Z]{2}"

    ra_match1 = re.match(ra_pattern1, line)
    ra_match2 = re.match(ra_pattern2, line)

    if not ra_match1 and not ra_match2:
        return False
    if ra_match1:
        ra = re.match(ra_pattern1, line).group(0)
    elif ra_match2:
        ra = re.match(ra_pattern2, line).group(0)
    code = re.search(code_pattern, line).group(0)

    return {"Name": "", "RA": ra, "group": cut_line(ra, code, line)}


# Insere o nome do aluno nos dicionários das turmas
def insert_name(classes, members_dataframe):
    for ra, name in members_generator(members_dataframe):
        for j in range(0, len(classes)):
            if classes[j]["RA"] == ra:
                classes[j]["Name"] = name

    return classes


# Abre o arquivo CSV e retorna um DataFrame com nomes e RAs
def open_csv(file):
    df = pd.read_csv(
        file,
        usecols=[2, 4],
        sep=",",
        encoding="utf-8",
        converters={"RA": lambda x: str(x)},
    )
    return df


# Seleciona o quadrimestre e o ano atuais
def select_date():
    date = datetime.today()
    period_1 = datetime(date.year, 5, 25)
    period_2 = datetime(date.year, 8, 25)
    print(f"\nData atual: {date.strftime('%d/%m/%Y')}")

    if date < period_1:
        period = "1"
    elif date < period_2:
        period = "2"
    else:
        period = "3"

    return period, date.strftime("%Y")


# Função principal
if __name__ == "__main__":
    period, year = select_date()
    csv_document = "RecadastroMembrosGTHC.csv"  # Arquivo de recadastro de membros
    url_ajuste = f"https://prograd.ufabc.edu.br/pdf/ajuste_{year}_{period}_matriculas_deferidas.pdf"  # Link do pdf das matrículas deferidas no ajuste
    url_reajuste = f"https://prograd.ufabc.edu.br/pdf/reajuste_{year}_{period}_matriculas_deferidas.pdf"  # Link do pdf das matrículas deferidas no reajuste
    print("=" * 60)
    print(f"Serão utilizados os PDFs do {period}º quadrimestre de {year}")
    print("=" * 60)
    raw_content_ajuste = get_content(url_ajuste)
    raw_content_reajuste = get_content(url_reajuste)
    raw_content = []

    if raw_content_ajuste and raw_content_reajuste:
        raw_content = raw_content_ajuste + raw_content_reajuste
    elif raw_content_ajuste:
        raw_content = raw_content_ajuste
    else:
        print(
            "Não foi possível acessar o PDF. Verifique se ele se encontra disponível ou se há conexão com a internet."
        )
        exit()

    content_in_lines = make_lines(raw_content)
    members_data = open_csv(csv_document)
    selected_lines = select_content(content_in_lines, members_data["RA"].tolist())
    complet_list = insert_name(selected_lines, members_data)
    pd.DataFrame(complet_list).to_csv("turmas.csv", index=False, sep=";")
