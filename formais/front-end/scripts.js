// Campos do formulario:
const variaveis = document.getElementById('variables')
const terminais = document.getElementById('end_symbols')
const inicial   = document.getElementById('first_symbol')
const producao  = document.getElementById('productions')

// Botoes:
const addProd   = document.getElementById('add_production')
const enviar    = document.getElementById('submit_form')

// Tabela de Producoes:
const tb_variaveis  = document.querySelectorAll(".tablecontent_end_symbols")
const producoes     = document.querySelectorAll(".tablecontent_productions")

addProd.addEventListener('click', ()=>{
    v = producao.split(" ")[0]
    p = producao.split(" ")[1]

    // Primeiro, mando pro back verificar se e uma producao valida
    input = {
        "variavel": v,
        "producao": p
    }

    fetch("/verifyProduction", {
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


    // Se for valida, adiciono a tabela de producoes no HTML

    // Verifica se ja ha a variavel no quadro
    hasVariable = false
    for(i=0; i<tb_variaveis.length; i++){
        if(v == tb_variaveis.innerHTML){
            hasVariable = true
        }
    }

    // Se ja nao tiver essa variavel no quadro, insere-a
    if(!hasVariable){
        novaVariavel = document.createElement('th')
        novaVariavel.innerHTML = v
        novaVariavel.setAttribute("class", "tablecontent_end_symbols")
        document.getElementById("table_end_symbols").appendChild(novaVariavel)
    }
})

enviar.addEventListener('click', ()=>{
        inputs = {
            "variaveis": variaveis,
            "terminal": terminais,
            "inicial": inicial,
            "producoes": producoes
        }

        fetch("/receiveInputs", {
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