import zipfile
import requests
from io import BytesIO
import os
import boto3

basepath = "./censup2019"

# Cria um diretório para armazenar o conteúdo do enade
os.makedirs(basepath, exist_ok=True)

print("Extracting data...")

# Define a url e faz o download do conteúdo
url = "https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2019.zip"
filebytes = BytesIO(requests.get(url, stream=True).content)

print("Unzip files...")
# Extrai o conteúdo do zipfile
myzip = zipfile.ZipFile(filebytes)
myzip.extractall(basepath)

print("BASE PATH....")
print(os.listdir(basepath))

# Pega a pasta "do meio" com caracteres esquisitos
pastadomeio = os.listdir(basepath)[-1]

print("ESTRUTURA DE PASTAS...")
print(basepath + '/' + pastadomeio + '/')
print(os.listdir(basepath + '/' + pastadomeio))

s3_client = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

print("Upload Censup IES to S3...")
s3_client.upload_file(
    basepath + "/" + pastadomeio + "/dados/MICRODADOS_CADASTRO_IES_2019.CSV", 
    "dl-langing-zone-809571664566", 
    "censup2019/ies/MICRODADOS_CADASTRO_IES_2019.CSV"
)

print("Upload Censup CURSO to S3...")
s3_client.upload_file(
    basepath + "/" + pastadomeio + "/dados/MICRODADOS_CADASTRO_CURSOS_2019.CSV", 
    "dl-langing-zone-809571664566", 
    "edsup2019/curso/MICRODADOS_CADASTRO_CURSOS_2019.CSV"
)


