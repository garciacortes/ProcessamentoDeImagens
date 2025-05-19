# app.py
import streamlit as st
from api import menu
from PIL import Image

def widgets(opcao, textInputs = [], numberInputs = [], selectBox = []):
    valores = {}
    imagem = None
    if opcao > 1:
        imagem = st.file_uploader("Escolha uma Imagem", type=["jpg", "png", "jpeg"])
    for nome in textInputs:
        valores[nome.lower()] = st.text_input(nome)
    for nome in numberInputs:
        valores[nome.lower()] = st.number_input(nome, step=0.5)
    if selectBox:
        menus = selectBox[:]
        menus[0] = "Selecione Uma Opção: "
        valores[selectBox[0].lower()] = st.selectbox(selectBox[0], menus)
    if st.button("enviar"):
        if (selectBox) and (valores[selectBox[0].lower()] == "Selecione Uma Opção: "):
            st.warning("Escolha uma opção valida")
            st.stop()
        if imagem is not None:
            valores["imagem"] = imagem.read()
        else:
            st.warning("Selecione Uma Imagem")
            st.stop()
        responseApi = menu(opcao, valores, st.session_state.token)
        if isinstance(responseApi, Image.Image):
            st.image(responseApi)
        else:
            st.text(responseApi)
        print(st.session_state.token)
    

def telas(opcao):
    match opcao:
        case 1:
            textInputs = ["texto"]
            widgets(opcao, textInputs)
        case 2:
            numberInputs = ["Altura", "Largura"]
            widgets(opcao, numberInputs = numberInputs)
        case 3:
            selectBox = ["Filtro", "Preto e Branco", "Sepia", "Inverter Cores", "Posterizar", "Solarizar", "Auto Contraste", "Equalizar"]
            widgets(opcao, selectBox = selectBox)
        case 4:
            widgets(opcao)
        case 5:
            numberInputs = ["Graus"]
            widgets(opcao, numberInputs=numberInputs)
        case 6:
            numberInputs = ["X", "Y", "Altura", "Largura"]
            widgets(opcao, numberInputs=numberInputs)
        case 7:
            numberInputs = ["Brilho", "Contraste"]
            widgets(opcao, numberInputs=numberInputs)
        case 8:
            widgets(opcao)
        case 9:
            textInputs = ["Texto"]
            numberInputs = ["Altura", "Largura", "TamanhoFonte"]
            widgets(opcao, textInputs, numberInputs)
        case 10:
            widgets(opcao)
        case 11:
            selectBox = ["filtro", "Media", "Gaussiano", "Mediana", "Sobel", "Laplaciano"]
            widgets(opcao, selectBox=selectBox)
        case 12:
            selectBox = ["Operacao", "Convolucao", "Correlacao"]
            widgets(opcao, selectBox=selectBox)
        case 13:
            selectBox = ["Tipo", "Low Pass", "High Pass", "Band Pass", "Notch"]
            widgets(opcao, selectBox=selectBox)
        case 14:
            selectBox = ["Tipo", "Limiarizacao", "Regiao", "Bordas", "Clustering"]
            widgets(opcao, selectBox=selectBox)
            
def main():
    
    if "busca_token" not in st.session_state:
        st.session_state.busca_token = True
    if "home" not in st.session_state:
        st.session_state.home = False
    if "token" not in st.session_state:
        st.session_state.token = None
        
    if st.session_state.busca_token:
        nome = st.text_input("Digite seu Nome")
        
        if st.button("Buscar Token"):
            resposta = menu(0, nome)
            if "token" in resposta and resposta["token"] != "ALUNO_NAO_LOCALIZADO":
                st.session_state.token = resposta["token"]
                st.session_state.busca_token = False
                st.session_state.home = True
                st.rerun()
            else:
                st.warning(resposta["token"])
                st.stop()
    elif st.session_state.home:
        menus = ["Selecione uma Opção", "Processar Texto", "Redimensionar Imagem", "Filtro de Imagem", "Imagem Cinza", "Rotacionar Imagem",
                    "Cortar Imagem", "Ajustar Imagem", "Histograma", "Colocar Texto Imagem", "Atualizar Foto",
                    "Processar Fitro", "Convulcao Correlacao", "Fourrier", "Segmentacao"]
                
        opcao = st.selectbox("MENU:", menus)
        telas(menus.index(opcao))
        

if __name__ == "__main__":  
    main()
