// Campos do formulario:
const variaveis = document.getElementById('variables')
const terminais = document.getElementById('end_symbols')
const inicial   = document.getElementById('first_symbol')
const producao  = document.getElementById('productions')

// Botoes:
const addProd   = document.getElementById('add_production')
const popProd   = document.getElementById('remove_production')
const upFile    = document.getElementById('insert_file')
const enviar    = document.getElementById('submit_form')
const limpar    = document.getElementById('clear_form')
const retornar  = document.getElementById('return_button')

function clearErrors(){
    let messages = [... document.querySelectorAll(".error_message")]
    messages.forEach((el) =>{
        el.parentNode.removeChild(el);
    })
    document.getElementById("error_message-area").style.display = "none"
}

function error_message(content){
    document.getElementById("error_message-area").style.display = "block"
    msgErro = document.createElement('p')
    msgErro.innerHTML = content
    msgErro.setAttribute("class", "error_message")
    document.getElementById("error_message-area").appendChild(msgErro)
}

addProd.addEventListener('click', ()=>{
    clearErrors()

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
            error_message("Formatação inválida de Produção<br>Deve ser informada no padrão Variável: Produção")
 

        }else{
            // Variavel e Producao:
            let variavel = producao.value.split(": ")[0]
            let prod = producao.value.split(": ")[1]

            // Pede pro back verificar se a producao utiliza apenas variaveis e terminais
            fetch("http://127.0.0.1:5000/verifyProduction", {
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
                        line = document.createElement('p')
                        line.setAttribute("class", "production_line")
                        line.innerHTML = variavel += "  &#8594;  " + prod + " "
                        document.getElementById("grammar-hint").appendChild(line)

                    }else{
                        if(lines[hasVariable].innerHTML.includes(" " + prod + " ")){
                            error_message("Esta produção já foi adicionada")
                        }else{
                            lines[hasVariable].innerHTML += "| " + prod + " "
                        }
                    }
                }
            })
        }     
    })
})


popProd.addEventListener('click', ()=>{
    clearErrors()

    input_inicial = {
        'entrada': producao.value
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
            error_message("Formatação inválida de Produção<br>Deve ser informada no padrão Variável: Produção")
        }else{
            // Variavel e Producao:
            let v = producao.value.split(": ")[0]
            let p = producao.value.split(": ")[1]
            let lines = [...document.querySelectorAll(".production_line")]

            for(let i=0; i < lines.length; i++){
                if(lines[i].innerHTML[0] == v){
                    if(lines[i].innerHTML.includes("| " + p + " ")){
                        lines[i].innerHTML = lines[i].innerHTML.replace("| " + p + " ", " ")
                    }else if(lines[i].innerHTML.includes(" " + p + " |")){
                        lines[i].innerHTML = lines[i].innerHTML.replace(" " + p + " |", "")
                    }else if(lines[i].innerHTML.includes(" " + p + " ")){
                        lines[i].parentNode.removeChild(lines[i])         
                    }else{
                        error_message("A variável " + v + " não contém esta produção")
                    }
                    return;
                }
            }

            error_message("Não há produções para a variável " + v)
            
        }
    })
})

limpar.addEventListener('click', ()=>{
    clearErrors()
    variaveis.value = ""
    terminais.value = "" 
    inicial.value = ""
    producao.value = ""
    producoes = [...document.querySelectorAll(".production_line")]
    producoes.forEach((el) => {
        el.parentNode.removeChild(el);
    })
})

upFile.addEventListener('change', ()=>{
    clearErrors()
    const file = upFile.files[0]

    // Cria um objeto FormData
    const formData = new FormData();
    formData.append('file', file); // Adiciona o arquivo ao FormData


    fetch("http://127.0.0.1:5000/uploadFile", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data['valid'] == false){
            error_message("Arquivo inválido<br>" + data['message'] + "<br>Por favor, tente novamente.")
        }
        else{
            let dict_returned = data['return']

            variaveis.value = dict_returned['variaveis']
            let variaveisArray = variaveis.value.split(',').map(v => v.trim());
            variaveis.value = variaveisArray.join(', ');

            terminais.value = dict_returned['terminais']
            let terminaisArray = terminais.value.split(',').map(v => v.trim());
            terminais.value = terminaisArray.join(', ');
            console.log(terminais.value)
            console.log(dict_returned['terminais'])

            inicial.value = dict_returned['inicial']

            // Limpa a caixa de texto das producoes
            producoes = [...document.querySelectorAll(".production_line")]
            producoes.forEach((el) => {
                el.parentNode.removeChild(el);
            })

            let ret_producoes = dict_returned['producoes']
            for (let key in ret_producoes){
                if (ret_producoes[key].length == 0){
                    continue;
                }
                let line = document.createElement('p')
                line.setAttribute("class", "production_line")
                line.innerHTML = key + "  &#8594;  " + ret_producoes[key]
                line.innerHTML = line.innerHTML.replace(",", " | ")
                document.getElementById("grammar-hint").appendChild(line)
            }
        }
    })
})

enviar.addEventListener('click', ()=>{
    clearErrors()
    document.getElementById("grammarPage").style.display = "none"
    document.getElementById("generationPage").style.display = "block"
})

retornar.addEventListener('click', ()=>{
    clearErrors()
    document.getElementById("generationPage").style.display = "none"
    document.getElementById("grammarPage").style.display = "block"
})
