import gradio as gr

get_local_storage = """
    function() {
      globalThis.setStorage = (key, value)=>{
        localStorage.setItem(key, value)
      }
       globalThis.getStorage = (key, value)=>{
        obtencion = localStorage.getItem(key)
        console.log("Dentro de getStorage:", obtencion)
        return obtencion
      }

       globalThis.cleanCred = (key, value)=>{
        localStorage.setItem(key, value)
      }

      globalThis.deductStore = (key, value)=>{
        new_value = ParseInt(value) - 1
        localStorage.setItem(key, new_value)
      }

      //Todo ésto lo hará al cargarse el load.

      //El token se deberá obtener de todas formas: 
      // Obtener la URL actual
        const urlActual = window.location;
        console.log("Hola")
        console.log(urlActual)

        // Buscar el parámetro "tkn"
        const urlParams = new URLSearchParams(window.location.search);
        console.log("Ésto es urlParams: ", urlParams)

        const token = urlParams.get('tkn');

        console.log("El token enviado es: ", token)

       if (!localStorage.getItem('tokens')) {
        console.log("Primera vez en el sistema, se le dan 5 tokens")
        localStorage.setItem('tokens', 5);
        //Para llegar a éste punto significa que no habían entrado sin embargo traían tokens, lo cual no se puede y está trucado.
        if(token){ 
            localStorage.setItem('trp', 'Ok')
            localStorage.setItem('tokens', 0)
            console.log("El usuario cargo la url sin haber usado el sitio, queda flagged como trampa y se le otorgan 0 tokens.")
            }
        }
        else
        {
            console.log("Ya tiene hecho el espacio para tokens, no es la primera vez que visita. Si podemos recargar, solo aquí:")
            console.log("token es: ", token)
            trap = localStorage.getItem('trp') 
            console.log("trap es: ", trap)
            credused = localStorage.getItem('credused')
            console.log("credused es: ", credused)

        if (token && trap === null && credused === null || token && trap === null && credused === "0") {
            console.log('Token encontrado hoy:', token);
            tokens_actuales = localStorage.getItem('tokens');
            console.log("Los tokens actuales que tienes son: ", tokens_actuales)
            nueva_cantidad = parseInt(tokens_actuales) + parseInt(token)
            localStorage.setItem('tokens', nueva_cantidad);
            localStorage.setItem('credused', 1)
            console.log("El usuario cargo sus tokens, se marca que ya usó ese crédito.")
        } 
        else { console.log('No se encontró el token'); }


        }

        //Al final obten cuantos tokens tiene.
        const legado = localStorage.getItem('tokens');

        

        return legado;
       
      }
    """

def predict(text_input, tokens_total):
   
    resultado_texto = "Hola " + text_input + ", éste es el resultado." 
    print("Esto es tokens_total: ", tokens_total)
    
    if int(tokens_total) > 0:
        print("Saldo Positivo")
        return tokens_total, resultado_texto, gr.Button(interactive=True), gr.Button(visible=False)

    else:
    
        print("Saldo negativo")
        return tokens_total, resultado_texto, gr.Button(interactive=False), gr.Button(visible=True)
    
def deduct(tokens_total):
  
   print("Estoy en deduct. Y esto es tokens_total: ", tokens_total)
   tokens_actualizados = int(tokens_total) - 1
   return tokens_actualizados


with gr.Blocks() as block:

    tokens_total = gr.Text(label="Tokens Disponibles", interactive = True)
    text_input = gr.Text(label="Tu Nombre:")
    resultadoFinal = gr.Text(label="Resultado")
   

    #text_input.change(None, tokens_label, tokens_label, js="(v)=>{ getStorage('text_input',v) }")
    #tokens_label.change(None, tokens_total, None, _js="(v)=>{ setStorage('otro',v) }")
    
    #resultadoFinal.change(None, text_input, resultadoFinal, js="(v)=>{ getStorage('text_input') }")
    btn = gr.Button("Enviar", icon="aiicon.png")
    payBtn = gr.Button("Buy Tokens", icon="aiicon.png", interactive = True, visible = True)

    btn.click(fn=predict, inputs=[text_input, tokens_total], outputs=[tokens_total, resultadoFinal, btn, payBtn])
    resultadoFinal.change(None, tokens_total, outputs=[tokens_total], _js="(v)=>{ deductStore('tokens', v) }")

    payBtn.click(None, inputs=None, outputs=None, _js="(v)=>{ cleanCred('credused',0) }" )
    
    block.load(
        None,
        inputs=None,
        outputs=[tokens_total],
        _js=get_local_storage,
    )

block.launch(debug=True)