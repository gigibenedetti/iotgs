import cv2
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime

cap = cv2.VideoCapture("ferrugem.mp4")

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
            <p class="fst-italic">Com base nas informações desse relatório, é possível utilizar os dados para definir a quantidade a ser utilizado do anti-fúngico em busca de minimizar o prejuízo que a doença, Ferrugem, causa nas plantações.</p>
            <p class="font-monospace">O fungo Puccinia spp. é o agente causal da ferrugem em várias espécies vegetais, como plantas olerícolas e gramíneas de importância econômica.
            <p class="font-monospace">Quando a doença ocorre em áreas que apresentam condições climáticas favoráveis, causa severas perdas por atacar todas as partes verdes da planta.</p>
            <p class="font-monospace">A ocorrência está vinculada a áreas onde as temperaturas são elevadas durante a primavera. Por esse motivo, não ocorre todos os anos em regiões de clima frio.</p>
            <p class="font-monospace">Os sintomas da Ferrugem:
            <ul class="list-group list-group-flush">
                <li class="list-group-item font-monospace">1. Aparecimento de manchas que surgem, numa primeira fase, na parte de cima da folha.</li>
                <li class="list-group-item font-monospace">2. As manchas podem ser amareladas, com um tom esverdeado ou alaranjado e vermelhas no centro.</li>
                <li class="list-group-item font-monospace">3. A parte inferior da folha pode conter caroços nas mesmas zonas onde surgem as manchas no topo. São nesses caroços que se encontram os esporos do fungo.</li>
                <li class="list-group-item font-monospace">4. Algumas semanas depois do aparecimento das manchas, elas adquirem uma textura poeirenta que indica que o fungo se está reproduzindo. As folhas mais atacadas podem ficar deformadas e cair prematuramente.</li>
            </ul>
            <button type="button" class="btn btn-secondary m-3" role="button" aria-disabled="true"><a href='./projetogs.html#Ferrugem' class="link-light">Como foi realizado este projeto?</a></button>
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
        nome_cell.string = 'Ferrugem'
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
     
    # Limite da cor para a ferrugem (tons de marrom, laranja e laranja claro)
    lower_brown = np.array([5, 50, 50])
    upper_brown = np.array([30, 255, 255])
    lower_light_orange = np.array([10, 50, 50])
    upper_light_orange = np.array([30, 255, 255])
 
    # Cria uma máscara para a região de interesse (ferrugem)
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    mask_light_orange = cv2.inRange(hsv, lower_light_orange, upper_light_orange)
  
    # Combina as máscaras de marrom e laranja claro
    mask = cv2.bitwise_or(mask_brown, mask_light_orange)

    # Aplica operações morfológicas para melhorar a máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Encontra os contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    result = cv2.bitwise_and(frame, frame, mask = mask)
    
    # Desenha os contornos encontrados com mais precisão
    for contour in contours:
        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
 
    cv2.imshow('frame', frame)
     
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    quantidade_doencas = len(contours)
    tamanho_doencas = [cv2.contourArea(contour) for contour in contours if cv2.contourArea(contour) > 0]
    relatorio_html = gerar_relatorio(quantidade_doencas, tamanho_doencas)

    # Salvar o relatório HTML em um arquivo
    with open('relatorioFerrugem.html', 'w', encoding='utf-8') as file:
        file.write(relatorio_html)
 
cv2.destroyAllWindows()
cap.release()