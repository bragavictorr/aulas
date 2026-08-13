from google import genai 

client = genai.Client(api_key="AQ.Ab8RN6LRCQEDxxqvhII-3nhV8Osf3j3TycchKx1BbL2bfyAOKg")

def pergunta_na_IA():
    interaction_id = None
    print("Digite sua dúvida. em breve um especialista irá atende")
    while True:
        pergunta_usuario  = input()

        if pergunta_usuario.lower == "sair:":
            break

        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=pergunta_usuario,
          
            system_instruction="Você é o atendente digital do python. seu objetivo é responder a pergunta do usuário e capturar as informaçoes básicas: nome, e-mail e telefone",
            previous_interction_id=interaction_id
        )

        interaction_id = interaction.id
    

        print("marta:"+(interaction.output_text))
        print("digite 'sair' se deseja encerrar o chat")