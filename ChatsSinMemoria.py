import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import time

warnings.filterwarnings("ignore")

# 🔐 Cargar variables desde el archivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ No se encontró OPENAI_API_KEY en el archivo .env")

# 🤖 Configuración del modelo OpenRouter
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model_name="meta-llama/llama-3.3-70b-instruct",
    temperature=0.9,
)

# 🗨️ Prompt del sistema (opcional)
Meta_prompt = """
"""

print("💬 Chatbot vía OpenRouter (escribe 'salir' para terminar)\n")

while True:
    user_input = input("👤 Tú: ")

    if user_input.lower() in ["salir", "exit", "quit"]:
        print("👋 Hasta luego.")
        break

    try:
        # Sin memoria: solo se envía el prompt base y la pregunta actual
        prompt = f"""
{Meta_prompt}

Usuario:
{user_input}
"""

        response = llm.invoke([HumanMessage(content=prompt)])

        try:
            # Caso normal (AIMessage)
            print(f"🤖 Bot: {response.content.strip()}\n")
            time.sleep(2)

        except AttributeError:
            # Compatibilidad con otros formatos de respuesta
            if isinstance(response, dict) and "content" in response:
                print(f"🤖 Bot: {response['content'].strip()}\n")
            elif isinstance(response, list) and len(response) > 0:
                print(f"🤖 Bot: {response[0].content.strip()}\n")
            else:
                print(f"🤖 Bot: {response}\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")