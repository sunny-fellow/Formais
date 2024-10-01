// Botões: 
const retornar      = document.getElementById('return_button')
const fast_mode     = document.getElementById('fast_mode')
const detailed_mode = document.getElementById('detailed_mode')
const derivar       = document.getElementById('derivate')
const retornaProd   = document.getElementById('button_return')
const geraNova      = document.getElementById('button_plus')
const recarrega     = document.getElementById('button_reload')

// Divs e Textos:
const prod_choice   = document.getElementById('prod_choice')
const fast_buttons  = document.getElementById('fast_mode_btn')
const label_mode    = document.getElementById('label_mode') 
const grammar_results = document.getElementById('grammar-results')

let mode = "fast"


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
        })
    })
}

retornar.addEventListener('click', ()=>{

    document.getElementById("generationPage").style.display = "none"
    document.getElementById("grammarPage").style.display = "block"
})

fast_mode.addEventListener('click', ()=>{

    fetch("http://127.0.0.1:5000/setFastMode")
    .then(response => response.json())
    .then(data => {
        
        if(fast_mode.classList.contains("unselected")){
            fast_mode.classList.remove("unselected")
            fast_mode.classList.add("selected")
            detailed_mode.classList.remove("selected")
            detailed_mode.classList.add("unselected")
        }

        prod_choice.style.display = "none"
        label_mode.innerHTML = "Geração Rápida:"
        document.getElementById("button_plus").style.display = "inline"
        mode = "fast"
        
    })
})

detailed_mode.addEventListener('click', ()=>{

    fetch("http://127.0.0.1:5000/setDetailedMode")
    .then(response => response.json())
    .then(data => {
        
        if(detailed_mode.classList.contains("unselected")){
            detailed_mode.classList.remove("unselected")
            detailed_mode.classList.add("selected")
            fast_mode.classList.remove("selected")
            fast_mode.classList.add("unselected")
        }
        prod_choice.style.display = "block"
        label_mode.innerHTML = "Geração Detalhada:"
        document.getElementById("button_plus").style.display = "none"
        setOptionsFor(data['initial'])
        mode = "detailed"
        
    })
})

derivar.addEventListener('click', ()=>{
    // Captura qual radio foi selecionado
    resposta_usuario = document.querySelector('input[name="production"]:checked').value
    if(grammar_results.lastChild != null){
        let penultimate_line    = grammar_results.lastChild.innerHTML
        let penultimate_string  = penultimate_line.split("  &#8594;  ")[penultimate_line.split("  &#8594;  ").length - 1]
    }else{
        let penultimate_string = document.getElementById("choice_title").innerHTML.split(" ")[4]
    }

    fetch("http://127.0.0.1:5000/derivate", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'cadeia': penultimate_string,
            'variavel': document.getElementById("choice_title").innerHTML.split(" ")[4],
            'opcao': resposta_usuario,
        })
    })
    .then(response => response.json())
    .then(data => {
        // Caso tenha linhas anteriores, remove o <br><br>
        if(grammar_results.firstChild != null){
            let penultimate_line = grammar_results.firstChild.innerHTML
            penultimate_line = penultimate_line.substring(0, penultimate_line.length - 9)
            grammar_results.firstChild.innerHTML = penultimate_line
        }


        if(data['finished'] == true){
            document.getElementById("options_box").style.display = "none"
            
            let first_line = document.createElement('p')
            first_line.innerHTML = penultimate_line + "  &#8594;  <b>" + data['result'] + "</b>  (FIM)<br><br>"
            grammar_results.insertBefore(grammar_results.firstChild, first_line)
            document.getElementById("prod_choice").style.display = "none"
            
        }else{
            let new_line = document.createElement('p')
            new_line.innerHTML = penultimate_line + "  &#8594;  <b>" + data['result'] + "</b><br><br>"
            grammar_results.insertBefore(grammar_results.firstChild, new_line)
            
            setOptionsFor(data['toDerivate'])
        }

        if(data['isTrap'] == true){
            document.getElementById("prod_choice").style.display = "none"
            document.createElement('p')
            let last_line = "<b>A cadeia " + data['result'] + " é uma armadilha, não é possível uma derivação conclusiva.</b>"
        }
    })
})