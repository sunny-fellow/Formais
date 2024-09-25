// Campos do formulario:
const variaveis = document.getElementById('variables')
const terminais = document.getElementById('end_symbols')
const inicial   = document.getElementById('first_symbol')
const producao  = document.getElementById('productions')
const remocao   = document.getElementById('remove_productions')

// Botoes:
const addProd   = document.getElementById('add_production')
const popProd   = document.getElementById('remove_production')
const enviar    = document.getElementById('submit_form')


addProd.addEventListener('click', ()=>{
    txt_ex = document.getElementById("example_table")
    table  = document.getElementById("production_table")

    txt_ex.setAttribute("display", "none")
    table.setAttribute("display", "flex")

    // Tabela de Producoes:
    const tb_variaveis  = document.querySelectorAll(".tablecontent_end_symbols")
    const producoes     = document.querySelectorAll(".tablecontent_productions")

    fetch("http://127.0.0.1:5000/verifyInput", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'entrada': producao.value})
    })
    .then(response => response.json())
    .then(data => {
        if (data['valid'] == false){
            // Mensagem de erro
            msgErro = document.createElement('span')
            msgErro.innerHTML = "Produção inválida!\nDeve ser informada no formato L: P\nEm que L é uma variável e P é uma produção"
            msgErro.setAttribute("class", "error_message")
            producao.nextSibling.after(msgErro)


        }else{
            // Variavel e Producao:
            v = producao.value.split(": ")[0]
            p = producao.value.split(": ")[1]

            // Primeiro, mando pro back verificar se e uma producao valida
            input = {
                "variavel": v,
                "producao": p
            }

            fetch("http://127.0.0.1:5000/verifyProduction", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(input)
            })
            .then(response => response.json())
            .then(data => {
                if (data['valid'] == false){
                    alert("Produção inválida!")
                    return

                }else{
                    // Se for valida, adiciono a tabela de producoes no HTML
                    // Verifica se ja ha a variavel no quadro
                    hasVariable = -1
                    for(let i=0; i<tb_variaveis.length; i++){
                        if(tb_variaveis[i].innerHTML == v){
                            hasVariable = i
                        }
                    }

                    // Se ja nao tiver essa variavel no quadro, insere-a
                    if(hasVariable == -1){
                        novaVariavel = document.createElement('th')
                        novaVariavel.innerHTML = v
                        novaVariavel.setAttribute("class", "tablecontent_end_symbols")
                        document.getElementById("table_end_symbols").appendChild(novaVariavel)

                        campoProducao = document.createElement('td')
                        campoProducao.setAttribute("class", "tablecontent_productions")
                        document.getElementById("table_productions").appendChild(campoProducao)

                        novaProducao = document.createElement('p')
                        novaProducao.innerHTML = p
                        campoProducao.appendChild(novaProducao)
                    }else{
                        // Se ja tiver essa variavel no quadro, insere a producao 
                        novaProducao = document.createElement('p')
                        novaProducao.innerHTML = p  
                        producoes[hasVariable].appendChild(novaProducao)
                    }
                }
            })
            .catch(error => {
                console.error('Erro:', error)
            })
        }
    })
})

popProd.addEventListener('click', ()=>{
    input_inicial = {
        'entrada': remocao.value
    }

    fetch("http://127.0.0.1:5000/verifyInput", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(input_inicial)
    })
    .then(response => response.json)
    .then(data => {
        if (data['valid'] == false){
            alert("Produção inválida!")
            return
        }else{
            // Variavel e Producao:
            v = remocao.value.split(": ")[0]
            p = remocao.value.split(": ")[1]

            // Primeiro, mando pro back verificar se e uma producao valida e remove-la
            input = {
                "variavel": v,
                "producao": p
            }

            fetch("http:///127.0.0.1:5000/removeProduction", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(input)
            })
            .then(response => response.json())
            .then(data => {
                if (data['valid'] == false){
                    alert("Produção inválida!")
                    return
                }else{
                    // Como a producao foi removida, removo-a da tabela de producoes
                    // Tabela de Producoes:
                    const tb_variaveis  = document.querySelectorAll(".tablecontent_end_symbols")
                    const producoes     = document.querySelectorAll(".tablecontent_productions")

                    for (let i=0; i<tb_variaveis.length; i++){
                        if(tb_variaveis[i].innerHTML == v){
                            for (let j=0; j<producoes[i].children.length; j++){
                                if(producoes[i].children[j].innerHTML == p){
                                    producoes[i].removeChild(producoes[i].children[j])
                                }
                            }
                            break;
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Erro:', error)
            })
        }
    })
})

enviar.addEventListener('click', ()=>{
    fetch("")

    producoes = {}
    const tb_variaveis = [... document.querySelectorAll(".tablecontent_end_symbols")]
    const producoes_p = [... document.querySelectorAll(".tablecontent_productions")]

    variaveis.value.split(", ").map((variavel) => {
        variavel != "epsilon" ? producoes[variavel] = [] : null;
    })

    for (let i=0; i < tb_variaveis.length; i++){
        variavel = tb_variaveis[i].innerHTML
        children = [...producoes_p[i].children]
        for(let j=0; j < children.length; j++){
            producoes[variavel].push(children[j].innerHTML)
        }
    }

 
    
    inputs = {
        "variaveis": variaveis.value.split(", "),
        "terminal": terminais.value.split(", "),
        "inicial": inicial.value,
        "producoes": producoes
    }

    console.log(inputs)

    fetch("http://127.0.0.1:5000/receiveInputs", {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputs)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        console.error('Erro:', error)
    })
    
})
