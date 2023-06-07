import cv2
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime

cap = cv2.VideoCapture("manchaalvo.mp4")

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
            <p class="fst-italic">Com base nas informações desse relatório, é possível utilizar os dados para definir a quantidade a ser utilizado do anti-fúngico em busca de minimizar o prejuízo que a doença, Mancha-Alvo, causa nas plantações.</p>
            <p class="font-monospace">Mancha alvo é uma doença foliar causada por um fungo chamado Corynespora cassiicola. Esta doença pode atacar diversas culturas. dentre as principais estão a soja e o algodão.</p>
            <p class="font-monospace">Apesar de ser um parossistema menos agressivo que a ferrugem da soja, em algumas cultivares tem causado perdas significativas quando não controlada.</p>
            <p class="font-monospace">Além disso, a doença parece estar mais agressivas nos últimos anos, pois as perdas em cultivares suscetíveis, que eram de 5 a 8 sc/ha, nas últimas safras têm sido de 10 a 15 sacas, atingindo até 20 sc/ha no último anos.</p>
            <p class="font-monospace">Os sintomas da Mancha-Alvo:

            <ul class="list-group list-group-flush">
                <li class="list-group-item font-monospace">1. Os primeiros sintomas são caracterizados por pequenas manchas circulares, com halo amarelado e um ponto negro no centro.</li>
                <li class="list-group-item font-monospace">2. O aumento das lesões em camadas circulares dá o aspecto de um "alvo".</li>
                <li class="list-group-item font-monospace">3. Em cultivares suscetíveis e condições de clima favorável, a evolução da doença pode ser rápida, induzindo desfolha prematura.</li>
            </ul>
            <button type="button" class="btn btn-secondary m-3" role="button" aria-disabled="true"><a href='./projetogs.html#Mancha-Alvo' class="link-light">Como foi realizado este projeto?</a></button>
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
        nome_cell.string = 'Mancha-Alvo'
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


while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    # Converte a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define as faixas de cores para os sintomas da mancha-alvo em HSV
    lower_circular_spot = np.array([0, 50, 50])
    upper_circular_spot = np.array([179, 255, 255])

    lower_yellow_halo = np.array([20, 50, 50])
    upper_yellow_halo = np.array([30, 255, 255])

 
    # Cria máscaras para filtrar os sintomas da mancha-alvo
    mask_circular_spot = cv2.inRange(hsv, lower_circular_spot, upper_circular_spot)
    mask_yellow_halo = cv2.inRange(hsv, lower_yellow_halo, upper_yellow_halo)

    # Combina as máscaras para obter a máscara final da mancha-alvo
    mask_target_spot = cv2.bitwise_and(mask_circular_spot, mask_yellow_halo)

    # Aplica operações morfológicas para melhorar a máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_target_spot = cv2.morphologyEx(mask_target_spot, cv2.MORPH_CLOSE, kernel)

    # Encontra os contornos na máscara
    contours, _ = cv2.findContours(mask_target_spot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    with open('relatorioMancha-Alvo.html', 'w', encoding='utf-8') as file:
        file.write(relatorio_html)
 
cv2.destroyAllWindows()
cap.release()

