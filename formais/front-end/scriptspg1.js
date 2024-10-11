/*

    O arquivo scriptspg1.js é responsável por controlar a página de inserção de gramáticas.
    Sua atribuição consiste em enviar os dados inseridos pelo usuário para o back-end, e por receber
    as respostas do back-end, exibindo-as na tela.
    Também contém elementos comuns as duas páginas, como o footer contendo informações sobre o grupo e o header,
    que entitula o nosso trabalho.

*/

// Campos do formulario:
const variaveis = document.getElementById('variables')              // Campo de input de variaveis   
const terminais = document.getElementById('end_symbols')            // Campo de input de terminais
const inicial   = document.getElementById('first_symbol')           // Campo de input do simbolo inicial
const producao  = document.getElementById('productions')            // Campo de input de producao

// Botoes:
const addProd   = document.getElementById('add_production')         // Botao de adicionar producao
const popProd   = document.getElementById('remove_production')      // Botao de remover producao
const upFile    = document.getElementById('insert_file')            // Botao de inserir arquivo
const enviar    = document.getElementById('submit_form')            // Botao de enviar formulario
const limpar    = document.getElementById('clear_form')             // Botao de limpar formulario


// Funcao para limpar as mensagens de erro
function clearErrors(){
    let messages = [... document.querySelectorAll(".error_message")]
    messages.forEach((el) =>{
        el.parentNode.removeChild(el);
    })
    document.getElementById("error_message-area").style.display = "none"
}

// Funcao para exibir mensagens de erro, recebe o conteudo da mensagem como parametro
function error_message(content){
    document.getElementById("error_message-area").style.display = "block"
    msgErro = document.createElement('p')
    msgErro.innerHTML = content
    msgErro.setAttribute("class", "error_message")
    document.getElementById("error_message-area").appendChild(msgErro)
}

/* ------------------- Eventos ------------------- */

// Evento de clique no botao de adicionar producao
addProd.addEventListener('click', ()=>{
    clearErrors()

    // Verifica se a producao foi inserida no formato correto
    fetch("http://127.0.0.1:5001/verifyInput", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'entrada': producao.value})
    })
    .then(response => response.json())
    .then(data => {
        if (data['valid'] == false){
            // Mensagem de erro caso a producao nao esteja no formato correto
            error_message("Formatação inválida de Produção<br>Deve ser informada no padrão Variável: Produção")
 

        }else{
            // Variavel e Producao:
            // Este split pelo ": " pode ser feito, porque a formatacao da producao foi verificada
            let variavel = producao.value.split(": ")[0]
            let prod = producao.value.split(": ")[1]


            // Pede pro back verificar se a producao utiliza apenas variaveis e terminais
            fetch("http://127.0.0.1:5001/verifyProduction", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'variaveis': variaveis.value,
                    'terminais': terminais.value,
                    'producao': prod
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data['valid'] == false){
                    // Se a producao usar simbolos invalidos, exibe mensagem de erro
                    error_message("Produção Inválida!<br>A produção deve utilizar apenas símbolos terminais e não terminais")
                }
                else{
                    // Verifica se ja ha a variavel no quadro
                    let lines = [...document.querySelectorAll(".production_line")]
                    hasVariable = -1
                    for(let i=0; i < lines.length; i++){
                        if(lines[i].innerHTML[0] == variavel){
                            hasVariable = i;
                            break;
                        }
                    }

                    // Se nao tiver essa variavel no quadro, insere-a
                    if(hasVariable == -1){
                        let line = document.createElement('p')
                        line.setAttribute("class", "production_line")
                        line.innerHTML = variavel + "  &#8594;  " + prod + " "
                        document.getElementById("grammar-hint-1").appendChild(line)

                    }else{
                        // Se ja tiver a variavel no quadro, verifica se a producao ja foi adicionada
                        // Se nao foi, adiciona
                        if(lines[hasVariable].innerHTML.includes(" " + prod + " ")){
                            error_message("Esta produção já foi adicionada")
                        }else{
                            lines[hasVariable].innerHTML += " | " + prod + " "
                        }
                    }


                    // Verifica se a variavel inserida eh a variavel inicial
                    if(inicial.value.length == 1 && inicial.value == variavel){
                        // Se for, primeiro procura a variavel inicial no quadro
                        let lines = [...document.querySelectorAll(".production_line")]
                        let recomposicao = []
                        lines.forEach((el)=>{
                            if (el.innerHTML[0] == variavel){
                                recomposicao.push(el)
                                el.parentNode.removeChild(el)
                                return;
                            }
                        })
    
                        // Depois, recebe as demais producoes e as coloca na ordem em que aparecem, removendo-as do quadro
                        lines =  [...document.querySelectorAll(".production_line")]
                        lines.forEach((el)=>{
                            recomposicao.push(el)
                            el.parentNode.removeChild(el)
                        })
    
                        // Por fim, insere as producoes reordenadas de volta no quadro
                        let campo = document.getElementById("grammar-hint-1")
                        recomposicao.forEach((el)=>{
                            campo.appendChild(el)
                        })
                    }
                }

            })
        }     
    })
})

// Evento de clique no botao de remover producao
popProd.addEventListener('click', ()=>{
    clearErrors()

    // Verifica se a producao foi inserida no formato correto
    fetch("http://127.0.0.1:5001/verifyInput", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'entrada': producao.value})
    })
    .then(response => response.json())
    .then(data => {
        if (data['valid'] == false){
            // Mensagem de erro caso a producao nao esteja no formato correto
            error_message("Formatação inválida de Produção<br>Deve ser informada no padrão Variável: Produção")

        }else{
            // Variavel e Producao:
            let v = producao.value.split(": ")[0]
            let p = producao.value.split(": ")[1]

            // Recebe o array de linhas de producoes possiveis do quadro
            let lines = [...document.querySelectorAll(".production_line")]

            // Procura a variavel no quadro
            for(let i=0; i < lines.length; i++){
                if(lines[i].innerHTML[0] == v){

                    if(lines[i].innerHTML.includes("| " + p + " ")){
                        // Verifica se esta no meio ou no final das producoes
                        lines[i].innerHTML = lines[i].innerHTML.replace("| " + p + " ", " ")
                    }else if(lines[i].innerHTML.includes(" " + p + " |")){
                        // Verifica se esta no inicio
                        lines[i].innerHTML = lines[i].innerHTML.replace(" " + p + " |", "")
                    }else if(lines[i].innerHTML.includes(" " + p + " ")){
                        // Verifica se eh a unica producao
                        lines[i].parentNode.removeChild(lines[i])         
                    }else{
                        // Caso nao tenha encontrado a producao na variavel informada, exibe mensagem de erro
                        error_message("A variável " + v + " não contém esta produção")
                    }

                    // Retorna, pois ja encontrou a variavel e fez a alteracao necessaria, caso tenha encontrado
                    return;

                }
            }

            // Se nao encontrou a variavel informada, exibe mensagem de erro
            error_message("Não há produções para a variável " + v)
            
        }
    })
})

// Evento de clique no botao de limpar formulario
limpar.addEventListener('click', ()=>{
    // Limpa a gramatica armazenada no back-end
    fetch("http://127.0.0.1:5001/cleanGrammar")
    clearErrors()

    // Limpa os campos do formulario
    variaveis.value = ""
    terminais.value = "" 
    inicial.value = ""
    producao.value = ""

    // Limpa as producoes do quadro
    producoes = [...document.querySelectorAll(".production_line")]
    producoes.forEach((el) => {
        el.parentNode.removeChild(el);
    })
})

upFile.addEventListener('change', ()=>{
    clearErrors()
    // Recebe o arquivo, a partir do input file no html
    const file = upFile.files[0]

    // Cria um objeto FormData
    const formData = new FormData();
    formData.append('file', file); // Adiciona o arquivo ao FormData


    // Envia o arquivo para o back-end
    fetch("http://127.0.0.1:5001/uploadFile", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data['valid'] == false){
            // printa a mensagem de erro recebida do back-end, caso haja
            error_message("Arquivo inválido<br>" + data['message'] + "<br>Por favor, tente novamente.")
        }
        else{
            try{
                // Recebe os dados da gramatica armazenada no back-end
                let dict_returned = data['return']

                // Preenche os campos do formulario com os dados recebidos

                // Trata as variaveis, para exibir de forma mais amigavel
                variaveis.value = dict_returned['variaveis']
                if(variaveis.value){
                    try{
                        let variaveisArray = variaveis.value.split(',').map(v => v.trim());
                        variaveis.value = variaveisArray.join(', ');
                    }catch(e){
                    }
                }
                
                // Trata os terminais, para exibir de forma mais amigavel
                terminais.value = dict_returned['terminais']
                if(terminais.value){
                    try{
                        let terminaisArray = terminais.value.split(',').map(v => v.trim());
                        terminais.value = terminaisArray.join(', ');
                    }catch(e){
                    }
                }

                // Preenche o simbolo inicial
                inicial.value = dict_returned['inicial']

                // Limpa a caixa de texto das producoes
                producoes = [...document.querySelectorAll(".production_line")]
                if(producoes){
                    producoes.forEach((el) => {
                        el.parentNode.removeChild(el);
                    })
                }
            

                // Preenche as producoes
                let ret_producoes = dict_returned['producoes']
                for (let key in ret_producoes){
                    if (ret_producoes[key].length == 0){
                        continue;
                    }
                    let line = document.createElement('p')
                    line.setAttribute("class", "production_line")
                    let str = ret_producoes[key].join(" | ")
                    line.innerHTML = key + "  &#8594;  " + str
                    document.getElementById("grammar-hint-1").appendChild(line)
                }
            }catch(e){
                // Caso haja erro na leitura dos dados recebidos, exibe mensagem de erro
                error_message("Erro ao ler os dados do arquivo<br>Por favor, tente novamente.")
            }
            
        }
    })
    .catch((error) => {
        // Caso haja erro no envio do arquivo, exibe mensagem de erro
        error_message("Erro ao enviar o arquivo<br>Confira a formatação do arquivo<br>Por favor, tente novamente.")
    })
})

enviar.addEventListener('click', ()=>{
    clearErrors()

    // Antes de enviar os dados para o back-end, limpa a gramatica armazenada
    fetch("http://127.0.0.1:5001/cleanGrammar")

    // Recebe os dados inseridos pelo usuario
    let variables = variaveis.value.split(',').map(v => v.trim());
    let terminals = terminais.value.split(',').map(v => v.trim());
    let initial = inicial.value

    // Recebe as linhas de producao
    let lines = [...document.querySelectorAll(".production_line")]

    // Verifica se ha producoes inseridas
    if (lines.length === 0) {
        error_message("Nenhuma produção foi adicionada.");
        return;
    }

    // Cria um dicionario com as producoes
    let producoes = {}

    // Separa as variaveis e as producoes
    lines.forEach((el) => {
        let sep = el.innerHTML.split("  ")
        let variavel = sep[0]
        let producao = sep[2]
        for (let i = 3; i < sep.length; i++){
            producao += " " + sep[i]
        }
        producao = producao.split(" | ")
        producao = producao.map(p => p.trim())
        producoes[variavel] = producao
    })

    // Envia os dados para o back-end
    fetch("http://127.0.0.1:5001/receiveInputs", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'variaveis': variables,
            'terminais': terminals,
            'inicial': initial,
            'producoes': producoes
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data['valid'] == false){
            // Exibe mensagem de erro, caso haja
            error_message("Erro ao enviar os dados para o servidor<br>" + data['message'])
        }else{
            // Caso nao haja erro, exibe a pagina de geracao de palavras
            document.getElementById("grammarPage").style.display = "none"
            document.getElementById("generationPage").style.display = "block"

            // Exibe as producoes inseridas na pagina de geracao de palavras
            let grammar_import = document.getElementById("grammar-hint-2")
            let lines = [...document.querySelectorAll(".production_line")]
            let exibitions = [...document.querySelectorAll(".exibition_line")]

            // Limpa as producoes exibidas na pagina de geracao de palavras
            if(exibitions){
                exibitions.forEach((el) => {
                    el.parentNode.removeChild(el)
                })
            }

            // Inicia, por padrao, no modo rapido
            document.getElementById("fast_mode").click()

            // Exibe as producoes na pagina de geracao de palavras
            lines.forEach((el) => {
                let line = document.createElement('p')
                line.innerHTML = el.innerHTML
                line.setAttribute("class", "exibition_line")
                grammar_import.appendChild(line)
            })

            // Exibe o botao de gerar cadeias com base na producao
            document.getElementsByClassName("depth-inputs")[0].style.display = "flex"
        }
    })
})