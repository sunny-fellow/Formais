// Botões: 
const retornar      = document.getElementById('return_button')
const fast_mode     = document.getElementById('fast_mode')
const detailed_mode = document.getElementById('detailed_mode')
const derivar       = document.getElementById('derivate')
const retornaProd   = document.getElementById('button_return')
const geraNova      = document.getElementById('button_plus')
const recarrega     = document.getElementById('button_reload')
const searchDeph    = document.getElementById('search_by_depth')

// Divs e Textos:
const prod_choice   = document.getElementById('prod_choice')
const fast_buttons  = document.getElementById('fast_mode_btn')
const label_mode    = document.getElementById('label_mode') 
const grammar_results = document.getElementById('grammar-results')

mode = "fast"

function setOptionsFor(variable){
    fetch("http://127.0.0.1:5000/getProductionsOf", {
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

function message(content, time){
    let msg = document.getElementById("chain_msg")
    msg.innerHTML = content
    msg.style.display = "block"

    setTimeout(()=>{
        msg.style.display = "none"
    }, time)
}

retornar.addEventListener('click', ()=>{
    location.reload()

})


recarrega.addEventListener('click', ()=>{
    if(mode == "detailed"){
        detailed_mode.click()
    }else{
        fetch('http://127.0.0.1:5000/cleanChainTree')
        fast_mode.click()
    }
})

retornaProd.addEventListener('click', ()=>{
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

    last_prod_arr = secondElement.innerHTML.split(" ")
    last_prod     = last_prod_arr[last_prod_arr.length - 1]
    

    fetch("http://127.0.0.1:5000/getVariableToDerivate", {
        'method': 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        'body': JSON.stringify({'producao': last_prod})
    })
    .then(response => response.json())
    .then(data => {
        setOptionsFor(data['variable'])
    })
})

fast_mode.addEventListener('click', ()=>{

    fetch("http://127.0.0.1:5000/setFastMode")
    .then(response => response.json())
    .then(data => {
        
        retornaProd.style.display = "none"
        if(fast_mode.classList.contains("unselected")){
            fast_mode.classList.remove("unselected")
            fast_mode.classList.add("selected")
            detailed_mode.classList.remove("selected")
            detailed_mode.classList.add("unselected")
        }

        mode = "fast"
        prod_choice.style.display = "none"
        if(data["allTrap"]){
            alert("A gramática apresentada não pode gerar produções válidas")
            message("A gramática apresentada não pode gerar produções válidas", 10000)
        }else{
            label_mode.innerHTML = "Geração Rápida:"
            geraNova.style.display = "inline"

            geraNova.click()
        }
    })
})

detailed_mode.addEventListener('click', ()=>{

    fetch("http://127.0.0.1:5000/setDetailedMode")
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
            message("A gramática apresentada não pode gerar produções válidas", 10000)
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

derivar.addEventListener('click', ()=>{
    //Captura qual radio foi selecionado
    let resposta_usuario = null

    try{
        resposta_usuario = document.querySelector('input[name="production"]:checked').value
    }catch(e){
        alert("É necessário escolher pelo menos uma produção para prosseguir com a derivação da cadeia")
        console.log(e)
        return;
    }
    

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

    fetch("http://127.0.0.1:5000/derivate", {
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


        if(data['finished'] == true){
            document.getElementById("options_box").style.display = "none"
            
            let first_line = document.createElement('p')
            let result = document.createElement('b')
            result.innerHTML = data["result"]
            const arrow = "  &#8594;  "
            first_line.innerHTML = penultimate_line
            first_line.innerHTML += arrow
            first_line.append(result)
            first_line.innerHTML += "<br><br>"

            message("FIM - Cadeia Encerrada", 4000)

            if(grammar_results.firstChild!=null){
                grammar_results.insertBefore(first_line, grammar_results.firstChild)          
            }else{
                grammar_results.appendChild(first_line)
            }
            document.getElementById("prod_choice").style.display = "none"
            
        }else{
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

        if(data['isTrap'] == true){
            if (grammar_results) {
                let last_line = document.createElement('p');
                let result = data['result'] || "resultado desconhecido";
                message(`<b>A cadeia ${result} é uma armadilha, não é possível uma derivação conclusiva.</b>`, 10000)
                
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

geraNova.addEventListener('click', ()=>{
    fetch("http://127.0.0.1:5000/generateFastChain")
    .then(response => response.json())
    .then(data => {
        console.log(data)
        let derivations = data['chain']
        if(derivations.length == 0){
            message("A gramática apresentada não tem mais produções válidas", 10000)
            geraNova.setAttribute("disabled", true)
            return;
        }

        str = derivations[0]
        for (let s of derivations.slice(1)){
            if(s == ""){
                s = "<b>epsilon</b>"
            }
            str += "  &#8594;  " + s
        }

        let new_line = document.createElement('p')
        new_line.innerHTML = str
        new_line.setAttribute("class", "production_line")
        grammar_results.appendChild(new_line)

    })
})

searchDeph.addEventListener('click', ()=>{
    let depth = document.getElementById('depth').value

    // Retira as producoes que ja estiverem na caixa
    children = [... grammar_results.children]
    children.forEach((el)=>{
        el.parentNode.removeChild(el)
    })

    fetch("http://127.0.0.1:5000/generateByDepth", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'depth': depth})
    })
    .then(response => response.json())
    .then(data => {
        let derivations = data['chain']
        if(derivations.length == 0){
            message("A gramática apresentada não tem mais produções válidas", 10000)
            geraNova.setAttribute("disabled", true)
            return;
        }

        // Recebe um array de arrays, onde cada array é uma progressão de derivações
        for (let derivation of derivations){
            str = derivation[0]
            for (let s of derivation.slice(1)){
                if(s == ""){
                    s = "<b>epsilon</b>"
                }
                str += "  &#8594;  " + s
            }

            let new_line = document.createElement('p')
            new_line.innerHTML = str
            new_line.setAttribute("class", "production_line")
            grammar_results.appendChild(new_line)
        }
    })
})