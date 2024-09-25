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
        console.log(data)
    })

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
        // Lembrar de verificar aqui se for valida
        console.log(data)
    })
    .catch(error => {
        console.error('Erro:', error)
    })


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
        console.log(data)
    })
})

enviar.addEventListener('click', ()=>{
        inputs = {
            "variaveis": variaveis,
            "terminal": terminais,
            "inicial": inicial,
            "producoes": producoes
        }

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
    }
)
