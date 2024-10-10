/*
    Este script é responsável por controlar a interação do usuário com a página de derivação de cadeias.
    Ele é responsável por enviar requisições ao servidor, que por sua vez, irá processar as informações
    e retornar as respostas necessárias para a derivação da cadeia.

*/

// Botões: 
const retornar      = document.getElementById('return_button')                  // Botão de retornar para a pagina inicial
const fast_mode     = document.getElementById('fast_mode')                      // Botão de modo rápido
const detailed_mode = document.getElementById('detailed_mode')                  // Botão de modo detalhado
const derivar       = document.getElementById('derivate')                       // Botão de derivação
const retornaProd   = document.getElementById('button_return')                  // Botão de retornar a produção
const geraNova      = document.getElementById('button_plus')                    // Botão de gerar nova cadeia
const recarrega     = document.getElementById('button_reload')                  // Botão de recarregar a geracao de cadeias
const searchDeph    = document.getElementById('search_by_depth')                // Botão de buscar por profundidade

// Divs e Textos:
const prod_choice     = document.getElementById('prod_choice')                  // Div de escolha de produção   
const fast_buttons    = document.getElementById('fast_mode_btn')                // Div de botões do modo rápido
const label_mode      = document.getElementById('label_mode')                   // Texto de modo de geração
const grammar_results = document.getElementById('grammar-results')              // Div de resultados
const depth_inputs    = document.getElementsByClassName('depth-inputs')[0]      // Div de inputs de profundidade
const spinner         = document.getElementById('loading-spinner')              // Spinner de carregamento

// Variavel que guarda o modo de geracao atual, util para botoes que dependem do modo
mode = "fast"


// Função que seta as opções de produção para a variável passada
function setOptionsFor(variable){
    fetch("http://127.0.0.1:5001/getProductionsOf", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'variavel': variable})
    })
    .then(response => response.json())
    .then(data => { 
        let options = data['productions']

        // Remove as opcoes anteriores
        let options_to_remove = [... document.querySelectorAll(".prod")]
        options_to_remove.forEach((el) =>{
            el.parentNode.removeChild(el);
        })

        // Adiciona as novas opcoes
        document.getElementById("choice_title").innerHTML = "Derivar a variável " + variable + " em:"
        options.forEach((el) =>{
            // Cria a div que contem o input e a label
            let div_option = document.createElement('div')
            div_option.setAttribute("class", "prod")

            // Cria o input
            let input_option = document.createElement('input')
            input_option.setAttribute("type", "radio")
            input_option.setAttribute("name", "production")
            input_option.setAttribute("id", "prod_" + el)
            input_option.setAttribute("value", el)

            // Cria a label
            let label_option = document.createElement('label')
            label_option.setAttribute("for", "prod_" + el)
            label_option.setAttribute("class", "prod-lbl")
            label_option.innerHTML = el
            if(data['traps'].includes(el)){
                label_option.classList.add("trap")
            }

            // Adiciona o input e a label na div
            div_option.appendChild(input_option)
            div_option.appendChild(label_option)

            // Adiciona a div na div de opcoes
            document.getElementById("options_box").appendChild(div_option)
            document.getElementById("options_box").style.display = "block"
        })
    })
}

// Função que exibe uma mensagem na tela por um tempo determinado
function message(content){
    let msg = document.getElementById("chain_msg")
    msg.innerHTML = content
    msg.style.display = "block"
}

function removeMessage(){
    let msg = document.getElementById("chain_msg")
    if(msg != null)
        msg.style.display = "none"
}


/* Eventos dos botões */


// Evento de clique no botão de retornar
retornar.addEventListener('click', ()=>{
    removeMessage()
    location.reload()
    fetch("http://127.0.0.1:5001/cleanGrammar")
    geraNova.removeAttribute("disabled")
})


// Evento de clique no botão de recarregar
recarrega.addEventListener('click', ()=>{
    removeMessage()
    let lines = [... grammar_results.children]
    lines.forEach((el)=>{
        el.parentNode.removeChild(el)
    })

    // Limpa a arvore de derivação
    fetch('http://127.0.0.1:5001/cleanStack')
    .then(()=>{
        geraNova.removeAttribute("disabled")
        if(mode == "detailed"){
            // Se estiver no modo detalhado, recarrega as opções
            detailed_mode.click()
        }else{
            // Se estiver no modo rápido, recarrega a cadeia
            fast_mode.click()
        }
    })
})

// Evento de clique no botão de retornar a produção
retornaProd.addEventListener('click', ()=>{
    // Pega os dois primeiros elementos da arvore de derivação
    let firstElement = null
    let secondElement = null

    // Objetivo: voltar a producao para a penultima, e mandar para o back, para
    // que ele informe qual a variavel que deveria ser derivada.
    
    // tenta pegar os dois primeiros paragrafos
    try{
        firstElement = grammar_results.firstChild
        secondElement = firstElement.nextSibling
        // caso o primeiro seja null e nao seja possivel procurar o proximo irmao, significa que esta na primeira producao
        // assim, o que se precisa fazer eh apenas resetar o modo detalhado
    }catch(e){
        detailed_mode.click()
        return;
    }

    // caso ele consiga ler o primeiro elemento, mas o segundo eh nulo, entao ha apenas uma producao na "pilha"
    // dessa forma, precisa-se apenas resetar o modo detalhado tambem
    if(secondElement == null){
        detailed_mode.click()
        return;
    }
    
    // remove o primeiro elemento da "pilha"
    firstElement.parentNode.removeChild(firstElement)
    secondElement.innerHTML += "<br><br>"

    // pega a ultima producao da arvore
    last_prod_arr = secondElement.innerHTML.split(" ")
    last_prod     = last_prod_arr[last_prod_arr.length - 1]
    

    // pergunta para o back qual a variavel que deveria ser derivada
    fetch("http://127.0.0.1:5001/getVariableToDerivate", {
        'method': 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        'body': JSON.stringify({'producao': last_prod})
    })
    .then(response => response.json())
    .then(data => {
        // Define as opcoes para a variavel retornada
        setOptionsFor(data['variable'])
        prod_choice.style.display = "flex"
    })
})

// Evento de clique no botão de modo rápido
fast_mode.addEventListener('click', ()=>{
    removeMessage()
    fetch("http://127.0.0.1:5001/cleanStack")
    
    // Remove acesso a funcionalidades apenas do modo detalhado, e ativa as do modo rápido
    depth_inputs.style.display = "flex"
    geraNova.removeAttribute("disabled")

    let lines = [... grammar_results.children]
    lines.forEach((el)=>{
        el.parentNode.removeChild(el)
    })

    // Manda para o back que o modo rápido foi ativado
    fetch("http://127.0.0.1:5001/setFastMode")
    .then(response => response.json())
    .then(data => {
        
        // Formata os estilos dos botoes, conforme qual estiver selecionado
        retornaProd.style.display = "none"
        if(fast_mode.classList.contains("unselected")){
            fast_mode.classList.remove("unselected")
            fast_mode.classList.add("selected")
            detailed_mode.classList.remove("selected")
            detailed_mode.classList.add("unselected")
        }

        // Ativa a caixa de Selecoes
        mode = "fast"
        prod_choice.style.display = "none"
        if(data["allTrap"]){
            // Se a gramatica nao tiver producoes validas, informa o usuario
            alert("A gramática apresentada não pode gerar produções válidas, todas as variáveis são armadilhas")
            message("A gramática apresentada não pode gerar produções válidas<br>Botão '+' desabilitado")
            geraNova.setAttribute("disabled", true)
        }else{
            // Formata o titulo adequado a caixa de producoes
            label_mode.innerHTML = "Geração Rápida:"
            geraNova.style.display = "inline"

            geraNova.click()
        }
    })
})

// Evento de clique no botão de modo detalhado
detailed_mode.addEventListener('click', ()=>{
    removeMessage()
    // Remove acesso a funcionalidades apenas do modo rápido, e ativa as do modo detalhado
    depth_inputs.style.display = "none"
    geraNova.removeAttribute("disabled")

    // Manda para o back que o modo detalhado foi ativado
    fetch("http://127.0.0.1:5001/setDetailedMode")
    .then(response => response.json())
    .then(data => {
        
        // Formata os estilos dos botoes, conforme qual estiver selecionado
        if(detailed_mode.classList.contains("unselected")){
            detailed_mode.classList.remove("unselected")
            detailed_mode.classList.add("selected")
            fast_mode.classList.remove("selected")
            fast_mode.classList.add("unselected")
        }

        mode = "detailed"
        // Retira as producoes que ja estiverem na caixa
        children = [... grammar_results.children]
        children.forEach((el)=>{
            el.parentNode.removeChild(el)
        })
        if(data["allTrap"]){
            message("A gramática apresentada não pode gerar produções válidas")
        }else{
            // Ativa a caixa de Selecoes
            prod_choice.style.display = "block"
            setOptionsFor(data['initial'])
    
            // Formata o titulo adequado a caixa de producoes
            label_mode.innerHTML = "Geração Detalhada:"
    
            // Remove o botao de adicionar
            geraNova.style.display = "none"
            
            // Torna o botao de retornar a producao visivel
            retornaProd.style.display = "inline"
        }
    })
})

// Evento de clique no botão de derivação
derivar.addEventListener('click', ()=>{
    //Captura qual radio foi selecionado
    let resposta_usuario = null

    // Tenta pegar o valor do radio selecionado
    try{
        resposta_usuario = document.querySelector('input[name="production"]:checked').value
    }catch(e){
        alert("É necessário escolher pelo menos uma produção para prosseguir com a derivação da cadeia")
        console.log(e)
        return;
    }
    
    // Pega a ultima palavra da ultima linha da arvore de derivação
    let last_word = ""
    if(grammar_results.firstChild != null){
        let penultimate_line    = grammar_results.firstChild.innerHTML
        let penultimate_string  = penultimate_line.split("  &#8594;  ")
        last_word = penultimate_string[penultimate_string.length - 1]
        last_word = last_word.split("<b>")[1]
        last_word = last_word.split("</b>")[0]
    }else{
        last_word = document.getElementById("choice_title").innerHTML.split(" ")[3]
    }

    // Manda para o back a palavra a ser derivada, a variavel que deveria ser derivada e a producao escolhida
    fetch("http://127.0.0.1:5001/derivate", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'cadeia': last_word,
            'variavel': document.getElementById("choice_title").innerHTML.split(" ")[3],
            'opcao': resposta_usuario,
        })
    })
    .then(response => response.json())
    .then(data => {
        let penultimate_line = last_word
        // Caso tenha linhas anteriores, remove o <br><br>
        if(grammar_results.firstChild != null){
            penultimate_line = grammar_results.firstChild.innerHTML

            penultimate_line = penultimate_line.substring(0, penultimate_line.length - 8) // Tira os <br>
            grammar_results.firstChild.innerHTML = penultimate_line
            penultimate_line = penultimate_line.replace("<b>", "")
            penultimate_line = penultimate_line.replace("</b>", "")
        }

        // Se a derivação foi concluída, exibe a mensagem de fim e desativa a caixa de opções
        if(data['finished'] == true){
            document.getElementById("options_box").style.display = "none"
            
            let first_line = document.createElement('p')
            let result = document.createElement('b')
            result.innerHTML = data["result"] || "epsilon"
            const arrow = "  &#8594;  "
            first_line.innerHTML = penultimate_line
            first_line.innerHTML += arrow
            first_line.append(result)
            first_line.innerHTML += "<br><br>"

            message("FIM - Cadeia Encerrada")

            // Insere sempre em formato de pilha, no inicio
            if(grammar_results.firstChild!=null){
                grammar_results.insertBefore(first_line, grammar_results.firstChild)          
            }else{
                grammar_results.appendChild(first_line)
            }
            document.getElementById("prod_choice").style.display = "none"
            
        }else{
            // Se a derivação não foi concluída, exibe a mensagem de derivação e atualiza as opções
            let new_line = document.createElement('p')

            const arrow = "  &#8594;  "
            let result = document.createElement('b')
            result.innerHTML = data['result']

            new_line.innerHTML = penultimate_line
            new_line.innerHTML += arrow
            new_line.append(result)
            new_line.innerHTML += "</b><br><br>"

            if(grammar_results.firstChild!=null){
                grammar_results.insertBefore(new_line, grammar_results.firstChild)          
            }else{
                grammar_results.appendChild(new_line)
            }
            
            setOptionsFor(data['toDerivate'])
        }

        // Se a cadeia é uma armadilha, exibe a mensagem de armadilha
        if(data['isTrap'] == true){
            if (grammar_results) {
                let last_line = document.createElement('p');
                let result = data['result'] || "resultado desconhecido";
                message(`<b>A cadeia ${result} é uma armadilha, não é possível uma derivação conclusiva.</b>`)

                prod_choice.style.display = "none"
                
                // Inserindo o novo parágrafo no início ou no final, dependendo do estado atual do elemento
                if (grammar_results.firstChild) {
                    grammar_results.insertBefore(last_line, grammar_results.firstChild);
                } else {
                    grammar_results.appendChild(last_line);
                }
            }
        }
    })
})

// Evento de clique no botão de gerar nova cadeia
geraNova.addEventListener('click', ()=>{
    removeMessage()
    
    if(mode == "fast_depth"){
        fetch("http://127.0.0.1:5001/getChainByDepth", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'depth': document.getElementById('depth').value})
        })
        .then(response => response.json())
        .then(data => {
            spinner.style.display = "none"
            let derivation = data['chain']
            if(derivation.length == 0){
                message("A gramática apresentada não tem mais produções nessa profundidade")
                geraNova.setAttribute("disabled", true)
                mode = "fast"
                return;
            }

            str = derivation[0]
            for (let s of derivation.slice(1)){
                if(s == ""){
                    s = "<b>epsilon</b>"
                }
                str += "  &#8594;  " + s
            }

            // Insere a nova linha na div de resultados
            let new_line = document.createElement('p')
            new_line.innerHTML = str
            new_line.setAttribute("class", "production_line")
            grammar_results.appendChild(new_line)
        })

        return;
    }

    // Requisita ao back uma nova cadeia
    fetch("http://127.0.0.1:5001/generateFastChain")
    .then(response => response.json())
    .then(data => {
        let derivations = data['chain']

        // Se nao houve nenhuma producao valida, significa que a gramatica nao tem mais producoes validas.
        // Pois ela sempre tenta gerar uma nova cadeia, e se nao consegue, significa que nao ha mais producoes validas
        if(derivations.length == 0){
            message("A gramática apresentada não tem mais produções válidas<br>Botão '+' desligado")
            alert("A gramática apresentada não tem mais produções válidas")
            geraNova.setAttribute("disabled", true)
            return;
        }

        // Recebe um array de arrays, onde cada um deles é uma progressão de derivações
        str = derivations[0]
        for (let s of derivations.slice(1)){
            if(s == ""){
                s = "<b>epsilon</b>"
            }
            str += "  &#8594;  " + s
        }

        // Insere a nova linha na div de resultados
        let new_line = document.createElement('p')
        new_line.innerHTML = str
        new_line.setAttribute("class", "production_line")
        grammar_results.appendChild(new_line)

        // Se a cadeia gerada é uma armadilha, exibe a mensagem de armadilha
        if(data['continue'] == false){
            v = data['continue']
            message("A gramática apresentada não tem mais produções válidas<br>Botão '+' desligado")
            alert("A gramática apresentada não tem mais produções válidas")
            geraNova.setAttribute("disabled", true)
        }
        
    })
})

// Evento de clique no botão de buscar por profundidade
searchDeph.addEventListener('click', ()=>{
    removeMessage()
    geraNova.removeAttribute("disabled")
    // Captura a profundidade desejada
    let depth = document.getElementById('depth').value
    
    // Trata o input de profundidade
    fetch("http://127.0.0.1:5001/verifyDepth", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'depth': depth})
    })
    .then(response => response.json())
    .then(data =>
    {
        if(data['valid'] == false){
            message(data["message"])
            return;
        }

        // Retira as producoes que ja estiverem na caixa
        children = [... grammar_results.children]
        children.forEach((el)=>{
            el.parentNode.removeChild(el)
        })

        // Manda para o back a profundidade desejada
        spinner.style.display = "block"
        fetch("http://127.0.0.1:5001/generateByDepth", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'depth': depth})
        })
        .then(response => response.json())
        .then(data => {
            spinner.style.display = "none"
            let derivation = data['chain']
            if(derivation.length == 0){
                message("A gramática apresentada não tem mais produções nessa profundidade")
                geraNova.setAttribute("disabled", true)
                return;
            }

            str = derivation[0]
            for (let s of derivation.slice(1)){
                if(s == ""){
                    s = "<b>epsilon</b>"
                }
                str += "  &#8594;  " + s
            }

            // Insere a nova linha na div de resultados
            let new_line = document.createElement('p')
            new_line.innerHTML = str
            new_line.setAttribute("class", "production_line")
            grammar_results.appendChild(new_line)
            mode = "fast_depth"
        })
    })  
})