// Após o registro de temperatura bem-sucedido
// Enviar uma requisição AJAX para atualizar a tabela de temperaturas
function atualizarTabelaTemperaturas() {
    fetch('/temperatura')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Limpar a tabela
            var tabelaTemperaturas = document.querySelector('#tabela-temperaturas tbody');
            tabelaTemperaturas.innerHTML = '';

            // Preencher a tabela com os novos dados
            data.temperaturas.forEach(function(temperatura) {
                var row = document.createElement('tr');
                row.innerHTML = `
                    <td>${temperatura[0]}</td>  <!-- Nome do equipamento -->
                    <td>${temperatura[1]}</td>  <!-- Temperatura 1 -->
                    <td>${temperatura[2]}</td>  <!-- Temperatura 2 -->
                    <td>${temperatura[3]}</td>  <!-- Data e Hora -->
                `;
                tabelaTemperaturas.appendChild(row);
            });
        })
        .catch(function(error) {
            console.error('Erro ao atualizar a tabela de temperaturas:', error);
        });
}

// Chamar a função para atualizar a tabela assim que a página carregar
atualizarTabelaTemperaturas();
