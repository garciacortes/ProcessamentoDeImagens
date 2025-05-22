import requests
import base64
from io import BytesIO
from PIL import Image

# Função para converter texto para Base64
def text_to_base64(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

# Função para converter Base64 de volta para texto
def base64_to_text(base64_text):
    return base64.b64decode(base64_text).decode('utf-8')

# Função para converter imagem para Base64
def image_to_base64(image):
    return base64.b64encode(image).decode('utf-8')

# Função para converter Base64 de volta para image
def base64_to_image(base64_image):
    '''with open(outputh_path, "wb") as image_file:
      image_file.write(base64.b64decode(base64_image))
      return outputh_path'''
    try:
      return Image.open(BytesIO(base64.b64decode(base64_image)))
    except:
        return "foto Atualizada com sucesso"

def requestPost(url, data, headers):
  # Enviar a requisição POST para o webhook
  return requests.post(url, json=data, headers=headers)

def process_text(response):
  if response.status_code == 200:
    # Exibir a resposta completa para depuração
    print("Resposta completa do webhook:", response.text)
    try:
        # Extrair o JSON da resposta
        response_data = response.json()

        # Verificar se o campo 'resposta' está presente na resposta
        if 'resposta' in response_data:
            inverted_base64 = response_data['resposta']

            # Desconverte o Base64 de volta para o texto original invertido
            inverted_text = base64_to_text(inverted_base64)

            # Exibe o texto invertido
            return f"texto Redimensionada: {inverted_text}"
        elif 'token' in response_data:
          return response_data
        else:
            return "Erro: campo 'resposta' ou 'token' não encontrado na resposta."
    except ValueError as e:
        return f"Erro ao tentar converter a resposta para JSON: {e}"
  else:
    return f"Erro na requisição: {response.status_code} - {response.text}"

def Imagens(response):
  if response.status_code == 200:
    # Exibir a resposta completa para depuração
    print("Resposta completa do webhook:", response.text)
    try:  
        # Extrair o JSON da resposta
        response_data = response.json()

        # Verificar se o campo 'resposta' está presente na resposta
        if 'resposta' in response_data:
            inverted_base64 = response_data['resposta']

            # Desconverte o Base64 de volta para o texto original invertido
            return base64_to_image(inverted_base64)
        else:
            return "Erro: campo 'resposta' ou não encontrado na resposta."
    except ValueError as e:
        return f"Erro ao tentar converter a resposta para JSON: {e}"
  else:
    return f"Erro na requisição: {response.status_code} - {response.text}" 

headers_base = {
        "Content-Type": "application/json"
      }

def getHeaders(token):
  headers = headers_base.copy()
  headers["Authorization"] = token
  return headers

def menu(opc, dataUser, token=None):
  
  if 'imagem' in dataUser:
    nomeImagem = dataUser["imagem"]
  
  match opc:
    case 0:
      
      url = "https://alunos.umg.com.br/webhook/token"
      
      data = {
         "nome": dataUser.upper()
      }
      
      response = requestPost(url, data, headers_base)
      return process_text(response)
    case 1:
      # URL do webhook
      url = "https://alunos.umg.com.br/webhook/processar"

      # Converte o texto para Base64
      texto_base64 = text_to_base64(dataUser["texto"])

      data = {
      "texto_base64": texto_base64
      }

      # Verificar se a requisição foi bem-sucedida
      response = requestPost(url, data, getHeaders(token))
      return process_text(response)
      #print(" ")
    case 2:
      url = "https://alunos.umg.com.br/webhook/redimensionar"

      image_base64 = image_to_base64(nomeImagem)

      #altura = int(input("Digite a altura da nova imagem: "))
      #largura = int(input("Digite a largura da nova imagem: "))

      data = {
          "texto_base64": image_base64,
          "altura": dataUser["altura"],
          "largura": dataUser["largura"]
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      #print(" ")
    case 3:
      url = "https://alunos.umg.com.br/webhook/filtro"

      image_base64 = image_to_base64(nomeImagem)

      '''filtros = ["Preto e Branco", "Sepia", "Inverter Cores", "Posterizar", "Solarizar", "Auto Contraste", "Equalizar"]
      print("-------------- filtros disponivel --------------")
      for filtro in filtros:
        print(f"{filtro}")

      filtro = input("Digite o filtro desejado: ").lower()'''
      
      filtros = {
        "Preto e Branco": "grayscale",
        "Sepia": "sepia",
        "Inverter Cores": "invert",
        "Posterizar": "posterize",
        "Solarizar": "solarize",
        "Auto Contraste": "autocontrast",
        "Equalizar": "equalize"
      }
      
      data = {
          "texto_base64": image_base64,
          "filtro": filtros[dataUser["filtro"]]
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 4:
      url = "https://alunos.umg.com.br/webhook/cinza"

      image_base64 = image_to_base64(nomeImagem)

      data = {
          "texto_base64": image_base64
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 5:
      url = "https://alunos.umg.com.br/webhook/rotacionar"

      image_base64 = image_to_base64(nomeImagem)

      data = {
          "texto_base64": image_base64,
          "grau": dataUser["graus"]
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
    case 6:
      url = "https://alunos.umg.com.br/webhook/corte"

      image_base64 = image_to_base64(nomeImagem)

      data = {
          "texto_base64": image_base64,
          "X": dataUser["x"],
          "Y": dataUser["y"],
          "LARGURA": dataUser["largura"],
          "ALTURA": dataUser["altura"]
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 7:
      url = "https://alunos.umg.com.br/webhook/ajustar"

      image_base64 = image_to_base64(nomeImagem)

      data = {
          "texto_base64": image_base64,
          "brilho": dataUser["brilho"],
          "contraste": dataUser["contraste"]
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 8:
      url = "https://alunos.umg.com.br/webhook/histograma"

      image_base64 = image_to_base64(nomeImagem)

      data = {
          "texto_base64": image_base64
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 9:
      url = "https://alunos.umg.com.br/webhook/texto_imagem"

      image_base64 = image_to_base64(nomeImagem)

      size = [dataUser["largura"], dataUser["altura"]]

      data = {
          "texto_base64": image_base64,
          "TEXTO": dataUser["texto"],
          "POSICAO": size,
          "TAMANHO_FONTE": dataUser["tamanhofonte"]
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 10:
      url = "https://alunos.umg.com.br/webhook/foto"

      image_base64 = image_to_base64(nomeImagem)

      data = {
          "texto_base64": image_base64
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 11:
      url = "https://alunos.umg.com.br/webhook/processar_filtros"

      image_base64 = image_to_base64(nomeImagem)
      
      filtros = [ "Media", "Gaussiano", "Mediana", "Sobel", "Laplaciano"]
      
      data = {
          "texto_base64": image_base64,
          "filtro": filtros.index(dataUser["filtro"]) + 1
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 12:
      url = "https://alunos.umg.com.br/webhook/convulcao_correlacao"

      image_base64 = image_to_base64(nomeImagem)

      data = {
          "texto_base64": image_base64,
          "tipo": dataUser["operacao"]
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 13:
      url = "https://alunos.umg.com.br/webhook/frequencia"

      image_base64 = image_to_base64(nomeImagem)

      tipos = ["Low Pass", "High Pass", "Band Pass", "Notch"]
      '''print("-------------- tipos disponivel --------------")
      for tipo in tipos:
        print(f"{tipo}")

      tipo = input("Digite o nome do tipo desejado: ")'''
      tipoSelect = dataUser["tipo"].split()[0].lower()

      data = {
          "texto_base64": image_base64,
          "tipo": tipoSelect
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    case 14:
      url = "https://alunos.umg.com.br/webhook/segmentacao"

      image_base64 = image_to_base64(nomeImagem)

      '''tipos = ["Limiarizacao", "Regiao", "Bordas", "Clustering"]
      print("-------------- tipos disponivel --------------")
      for tipo in tipos:
        print(f"{tipo}")

      tipo = input("Digite o nome do tipo desejado: ").lower()'''

      data = {
          "texto_base64": image_base64,
          "tipo": dataUser["tipo"].lower()
      }

      response = requestPost(url, data, getHeaders(token))
      return Imagens(response)
      print(" ")
    #case _default:
      #break

menus = ["Processar Texto", "Redimensionar Imagem", "Filtro de Imagem", "Imagem Cinza", "Rotacionar Imagem",
        "Cortar Imagem", "Ajustar Imagem", "Histograma", "Colocar Texto Imagem", "Atualizar Foto",
        "Processar Fitro", "Convulcao Correlacao", "Fourrier", "Segmentacao"]

'''
while True:
  print("------------------- MENU -------------------")
  for i, opc in enumerate(menus):
    print(f"{i + 1}- {opc}")
  print("Qualquer opcao invalida - sair")
  print(" ")
  opcao = int(input("Digite a opcao: "))
  menu(opcao)
'''


