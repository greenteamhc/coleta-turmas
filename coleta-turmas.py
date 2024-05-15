import io
import re
import requests
import PyPDF2
import pandas as pd

# TODO: Otimizar o código
# TODO: Automatizar a busca do PDF de matrículas deferidas para o ajuste e reajuste


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

    for line in lines:
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
    for i in range(0, len(members_dataframe)):
        for j in range(0, len(classes)):
            if classes[j]["RA"] == members_dataframe["RA"][i]:
                classes[j]["Name"] = members_dataframe["Nome completo"][i]
    return classes


# Abre o arquivo CSV e retorna um DataFrame com nomes e RAs
def open_csv(file):
    df = pd.read_csv(
        file, usecols=[2, 4], encoding="utf-8", converters={"RA": lambda x: str(x)}
    )
    return df


# Função principal
if __name__ == "__main__":
    csv_document = "RecadastroMembrosGTHC.csv"  # Arquivo de recadastro de membros
    url_ajuste = "https://prograd.ufabc.edu.br/pdf/2024_1_matriculas_deferidas_pos_ajuste.pdf"  # Link do pdf das matrículas deferidas no ajuste
    url_reajuste = "https://prograd.ufabc.edu.br/pdf/reajuste_2024_1_matriculas_deferidas.pdf"  # Link do pdf das matrículas deferidas no reajuste

    raw_content_ajuste = get_content(url_ajuste)
    raw_content_reajuste = get_content(url_reajuste)
    raw_content = []

    if raw_content_ajuste and raw_content_reajuste:
        raw_content = raw_content_ajuste + raw_content_reajuste
    elif raw_content_ajuste:
        raw_content = raw_content_ajuste
    else:
        print("Não foi possível acessar o arquivo")

    content_in_lines = make_lines(raw_content)
    members_data = open_csv(csv_document)
    selected_lines = select_content(content_in_lines, members_data["RA"].tolist())
    complet_list = insert_name(selected_lines, members_data)
    pd.DataFrame(complet_list).to_csv("turmas.csv", index=False, sep=";")
