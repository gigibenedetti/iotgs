import cv2
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
cap = cv2.VideoCapture("sigatoka.mp4")

# Função para gerar o relatório HTML
def gerar_relatorio(quantidade_doencas, tamanho_doencas):
    # Criação do objeto BeautifulSoup com o template HTML
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Doenças</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            .sorted {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container mx-auto p-5">
            <h1 class="font-monospace text-center">Relatório de Doenças</h1>
            <h2 class="font-monospace text-center">Quantidade de plantas infectadas: {quantidade_doencas} Metro infectado: {sum_tamanho_doencas_m_formatted}</h2>
            <p class="fst-italic">Com base nas informações desse relatório, é possível utilizar os dados para definir a quantidade a ser utilizado do anti-fúngico em busca de minimizar o prejuízo que a doença, Sigatoka Negra, causa nas plantações de bananeira.</p>
            <p class="font-monospace">A sigatoka negra é uma doença fúngica, causada pelo fungo Mycosphaerella fijiensis Morelet, sendo sua forma anamórfica Paracercospora fijiensis (Morelet) Deighton. A sigatoka negra apareceu pela primeira vez em fevereiro de 1998 no Brasil nos municípios de Tabatinga e Benjamin Constant no Amazonas, seguindo para o Acre, Rondônia, Pará, Mato Grosso em 1999 e após 6 anos foi constatada pelo Instituto Biológico, no Estado de São Paulo, primeiramente em Miracatu em 22 de junho de 2004, onde nas três amostras enviadas das cultivares Galil 7, Nam e Galil 18, foram constatadas a Mycosphaerella fijiensis agente causal da Sigatoka Negra.</p>
            <p class="font-monospace">A Sigatoka Negra propaga-se por meio de dois tipos de esporos, conhecidos como conídios e ascósporos. A duração do ciclo de vida do fungo é influenciada principalmente pelas condições climáticas, tipo de hospedeiro e manejo da cultura. Os esporos germinam, se houver água livre sobre a folha, em menos de duas horas e os primeiros sintomas podem aparecer após 17 dias. A disseminação do fungo é influenciada por fatores ambientais tais como: umidade, luminosidade, temperatura e vento, sendo que o vento e a umidade na forma de chuva são os principais responsáveis pela liberação dos esporos e disseminação da doença. A maior forma de disseminação se dá por meio das folhas infectadas.</p>
            <p class="font-monospace">Os sintomas da Sigatoka Negra variam em função do estágio de desenvolvimento da planta, da suscetibilidade da cultivar e da severidade do ataque. São observados seis estágios de desenvolvimento da doença:

            <ul class="list-group list-group-flush">
                <li class="list-group-item font-monospace">1. Pequenas descolorações ou pontuações despigmentadas, menores que 1 mm, visíveis, na página inferior da folha</li>
                <li class="list-group-item font-monospace">2. Estrias de coloração marrom-clara, com 2 a 3 mm de comprimento</li>
                <li class="list-group-item font-monospace">3. As estrias se alongam e já podem ser visualizadas em ambas as faces da folha</li>
                <li class="list-group-item font-monospace">4. Manchas ovais de cor marrom escura na face inferior e negra na face superior da folha</li>
                <li class="list-group-item font-monospace">5. Manchas negras, com pequeno halo amarelo e centro deprimido</li>
                <li class="list-group-item font-monospace">6. Manchas com centro deprimido e de coloração branco acinzentado, que se coalescem em períodos favoráveis ao desenvolvimento do fungo.</li>
            </ul>
            <button type="button" class="btn btn-secondary m-3" role="button" aria-disabled="true"><a href='./projetogs.html#sigatoka' class="link-light">Como foi realizado este projeto?</a></button>
        <div class="mx-auto p-5">    
            <table class="table table-bordered border-black table-success sorted-asc">
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Nome da Doença</th>
                        <th>Tamanho do Sintoma <button class="btn btn-link" onclick="sortTable()"><i class='fas fa-sort toggle-sort'></button></th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
        </div>
        
        <script>
            function sortTable() {
                var table = document.querySelector("table");
                var tbody = table.querySelector("tbody");
                var rows = Array.from(tbody.getElementsByTagName("tr"));
                var sorted = rows.sort(function(a, b) {
                    var aSize = parseInt(a.lastElementChild.innerText);
                    var bSize = parseInt(b.lastElementChild.innerText);
                    return aSize - bSize;
                });

                // Check if the table is already sorted in ascending order
                var isSortedAscending = table.classList.contains("sorted-asc");

                if (isSortedAscending) {
                    sorted.reverse();
                    table.classList.remove("sorted-asc");
                    table.classList.add("sorted-desc");
                } else {
                    table.classList.remove("sorted-desc");
                    table.classList.add("sorted-asc");
                }

                tbody.innerHTML = "";
                sorted.forEach(function(row) {
                    tbody.appendChild(row);
                });
            }
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/js/all.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

    # Criação do objeto BeautifulSoup a partir do template HTML
    soup = BeautifulSoup(html_template, 'html.parser')

    # Adicionando a data e hora de execução
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    quantidade_cell = soup.new_tag('td')
    quantidade_cell.string = str(quantidade_doencas)

    # Adicionando os dados na tabela
    table_body = soup.find('tbody')

    rows = ''

    # Adicionando os valores de tamanho_doencas na tabela
    for tamanho in tamanho_doencas:
        row = soup.new_tag('tr')
        
        # Cria uma nova tag data_cell para cada iteração
        data_cell = soup.new_tag('td')
        data_cell.string = current_datetime
        row.append(data_cell)
        
        # Adiciona uma nova tag para o nome da doença (vazio neste exemplo)
        nome_cell = soup.new_tag('td')
        nome_cell.string = 'Sigatoka'
        row.append(nome_cell)
        
        # Cria uma nova tag tamanho_cell para cada iteração
        tamanho_cell = soup.new_tag('td')
        tamanho_cell.string = f'{round(tamanho,2)} cm'
        row.append(tamanho_cell)

        rows += str(row)
        sum_tamanho_doencas_cm = sum(tamanho_doencas)
        sum_tamanho_doencas_m = sum_tamanho_doencas_cm / 100
        sum_tamanho_doencas_m_formatted = "{:.2f}".format(sum_tamanho_doencas_m)

    table_body.append(BeautifulSoup(rows, 'html.parser'))

    # Atualiza a quantidade de doenças no cabeçalho
    h2 = soup.find('h2')
    h2.string = f"Quantidade de plantas infectadas: {quantidade_doencas} Metro infectado: {sum_tamanho_doencas_m_formatted}"

    
    # Retorna o relatório HTML
    return str(soup)

quantidade_doencas = 0
tamanho_doencas = []

while(1):
    ret, frame = cap.read()

    if not ret:
        break
    # Converte a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define as faixas de cores para os sintomas da Sigatoka em HSV
    lower_discoloration = np.array([0, 0, 0])
    upper_discoloration = np.array([179, 50, 50])

    lower_brown_streaks = np.array([10, 50, 50])
    upper_brown_streaks = np.array([30, 255, 255])

    lower_dark_brown_spots = np.array([0, 0, 0])
    upper_dark_brown_spots = np.array([179, 50, 50])

    lower_black_spots = np.array([0, 0, 0])
    upper_black_spots = np.array([179, 50, 50])

    lower_white_spots = np.array([0, 0, 0])
    upper_white_spots = np.array([179, 50, 50])

    # Cria máscaras para filtrar os sintomas da Sigatoka
    mask_discoloration = cv2.inRange(hsv, lower_discoloration, upper_discoloration)
    mask_brown_streaks = cv2.inRange(hsv, lower_brown_streaks, upper_brown_streaks)
    mask_dark_brown_spots = cv2.inRange(hsv, lower_dark_brown_spots, upper_dark_brown_spots)
    mask_black_spots = cv2.inRange(hsv, lower_black_spots, upper_black_spots)
    mask_white_spots = cv2.inRange(hsv, lower_white_spots, upper_white_spots)

    # Combina as máscaras para obter a máscara final da Sigatoka
    mask_sigatoka = cv2.bitwise_or(mask_discoloration, mask_brown_streaks)
    mask_sigatoka = cv2.bitwise_or(mask_sigatoka, mask_dark_brown_spots)
    mask_sigatoka = cv2.bitwise_or(mask_sigatoka, mask_black_spots)
    mask_sigatoka = cv2.bitwise_or(mask_sigatoka, mask_white_spots)

    # Aplica operações morfológicas para melhorar a máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_sigatoka = cv2.morphologyEx(mask_sigatoka, cv2.MORPH_CLOSE, kernel)

    # Encontra os contornos na máscara
    contours, _ = cv2.findContours(mask_sigatoka, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
 
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    quantidade_doencas = len(contours)
    tamanho_doencas = [cv2.contourArea(contour) for contour in contours if cv2.contourArea(contour) > 0]
    relatorio_html = gerar_relatorio(quantidade_doencas, tamanho_doencas)

    # Salvar o relatório HTML em um arquivo
    with open('relatorioSigatoka.html', 'w', encoding='utf-8') as file:
        file.write(relatorio_html)

    


cv2.destroyAllWindows()
cap.release()