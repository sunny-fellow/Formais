// Campos do formulario:
const variaveis = document.getElementById('variables')
const terminais = document.getElementById('end_symbols')
const inicial   = document.getElementById('first_symbol')
const producao  = document.getElementById('productions')

// Botoes:
const addProd   = document.getElementById('add_production')
const popProd   = document.getElementById('remove_production')
const enviar    = document.getElementById('submit_form')


addProd.addEventListener('click', ()=>{
    if (document.querySelector(".error_message")){
        document.getElementById("grammarInput").removeChild(document.querySelector(".error_message"))
    }

    // Tabela de Producoes:
    const tb_variaveis  = [...document.querySelectorAll(".tablecontent_end_symbols")]
    const producoes     = [...document.querySelectorAll(".table_productions")]

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
        if (data['valid'] == false){
            // Mensagem de erro
            msgErro = document.createElement('p')
            msgErro.innerHTML = "Producao invalida!<br>Deve ser informada no formato L: P*<br>Em que L e uma variavel e P* e uma producao"
            msgErro.setAttribute("class", "error_message")
            document.getElementById("add_production").after(msgErro)


        }else{
            // Variavel e Producao:
            variavel = producao.value.split(": ")[0]
            prod = producao.value.split(": ")[1]

            txt_ex = document.getElementById("example_table")
            table  = document.getElementById("production_table")

            txt_ex.style.display = "none"; 
            table.style.display = "flex";
            // Se for valida, adiciono a tabela de producoes no HTML
            // Verifica se ja ha a variavel no quadro
            hasVariable = -1
            for(let i=0; i<tb_variaveis.length; i++){
                if(tb_variaveis[i].innerHTML == variavel){
                    hasVariable = i
                    console.log("Variavel ja existe no quadro, na posicao: ", hasVariable)
                    break;
                }
            }

            // Se ja nao tiver essa variavel no quadro, insere-a
            if(hasVariable == -1){
                novaVariavel = document.createElement('th')
                novaVariavel.innerHTML = variavel
                novaVariavel.setAttribute("class", "tablecontent_end_symbols")
                document.getElementById("table_end_symbols").appendChild(novaVariavel)

                campoProducao = document.createElement('td')
                campoProducao.setAttribute("class", "tablecontent_productions")
                document.getElementById("table_productions").appendChild(campoProducao)

                novaProducao = document.createElement('p')
                novaProducao.innerHTML = prod
                campoProducao.appendChild(novaProducao)
                

            }else{
                // Se ja tiver essa variavel no quadro, insere a producao 
                novaProducao = document.createElement('p')
                novaProducao.innerHTML = prod 
                aux = [...document.querySelectorAll(".tablecontent_productions")][hasVariable]
                aux.appendChild(novaProducao)
            }
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
            alert("Producao invalida!")
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
                    alert("Producao invalida!")
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
    console.log("Enviando dados para o back-end")
    producoes = {}
    const tb_variaveis = [... document.querySelectorAll(".tablecontent_end_symbols")]
    const producoes_p = [... document.querySelectorAll(".tablecontent_productions")]

    fetch("http://127.0.0.1:5000/verifyInputGrammar", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'variaveis': variaveis.value, 
            'terminais': terminais.value, 
            'inicial': inicial.value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data['valid'] == false){
            erro_msg = document.createElement('p')
            erro_msg.innerHTML = "Erro na formatacao!<br>Mensagem de Erro: " + data['message']
            enviar.after(erro_msg)
        }else{
            for (let i=0; i < tb_variaveis.length; i++){
                producoes[tb_variaveis[i].innerHTML] = []
                variavel = tb_variaveis[i].innerHTML
                children = [...producoes_p[i].children]
                for(let j=0; j < children.length; j++){
                    producoes[variavel].push(children[j].innerHTML)
                }
            }
            
            console.log(variaveis.value)
            inputs = {
                "variaveis": variaveis.value,
                "terminais": terminais.value,
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
                if (data['valid'] == false){
                    erro_msg = document.createElement('p')
                    erro_msg.innerHTML = "Erro na gramatica!<br>Mensagem de Erro: " + data['message']
                    console.log("Erro na gramatica!<br>Mensagem de Erro: " + data['message'])
                }else{
                    document.getElementById("page1").style.display = "none"
                    document.getElementById("page2").style.display = "flex"
                    console.log(data)
                }
            })
            .catch(error => {
                console.error('Erro:', error)
            })
        }
    })
})