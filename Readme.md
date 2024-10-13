
---

# Gerador de Cadeias para Gramáticas Livres de Contexto

### Projeto Final - Disciplina: Linguagens Formais e Computabilidade  
#### Ciência da Computação - 3º Período, UFPB

**Participantes**:  
- [Herick Freitas](https://github.com/Herickjf)  
- [Lael Gustavo](https://github.com/sunny-fellow)  
- [Luis Reis](https://github.com/LuisReis09)  

---

## Descrição do Projeto

Este projeto tem como objetivo desenvolver um gerador de cadeias para gramáticas livres de contexto, que permite trabalhar com diferentes modos de derivação. Ele é dividido em duas áreas principais: **input de dados** e **output**.

### Funcionalidades do Input

No input, o usuário pode inserir a gramática de duas formas:
1. **Upload de arquivo** contendo a gramática.
2. **Preenchimento manual** dos dados diretamente no formulário HTML.

### Modos de Operação

O projeto oferece duas maneiras de trabalhar com a gramática inserida:

- **Modo Rápido**:
  - O usuário pode solicitar cadeias geradas 1 a 1, e o servidor fornecerá as cadeias conforme forem solicitadas.
  - É possível determinar uma profundidade de derivação específica, o que retornará as cadeias com essa quantidade de derivações, uma por uma, conforme solicita-se mais ao pressionar o botão '+'.

- **Modo Detalhado**:
  - Neste modo, o usuário tem controle total sobre a geração da cadeia. Ele pode escolher manualmente, para cada variável, qual produção será derivada. Isso oferece a liberdade de gerar cadeias passo a passo, com total controle sobre o processo.

### Linguagens e Tecnologias Utilizadas

- **Front-end**:
  - Figma
  - HTML
  - CSS
  - JavaScript

- **Ligação Front-Back**:
  - JavaScript

- **Back-end**:
  - Python

---

### **OBS: Para rodar localmente**

1. **Instalar o Live Server**  
   - Instale a extensão *Live Server* no ambiente de desenvolvimento *Visual Studio Code*.

2. **Atualizar o pip**  
   - Para garantir a versão mais recente do pip, rode o script `get-pip.py`.  
   - Se estiver utilizando **Ubuntu**, execute o comando:

     ```bash
     sudo python3 get-pip.py
     ```

3. **Instalar as dependências**  
   - As bibliotecas necessárias são *Flask* e *Flask-CORS*. Instale-as utilizando os seguintes comandos:

     ```bash
     pip install flask
     pip install flask_cors
     ```

4. **Executar o servidor**  
   - Navegue até o diretório `./back-end` e execute o servidor com o seguinte comando:
   
     - No **Windows**:

       ```bash
       py main.py
       ```

     - No **Linux**:

       ```bash
       python3 main.py
       ```

5. **Abrir a página**  
   - Abra o arquivo HTML principal utilizando o *Live Server* para visualizar o projeto em execução no navegador.

---
