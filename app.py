from flask import Flask, request, jsonify, render_template
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

print("Starting Flask app...")  # Debugging statement

app = Flask(__name__)

# Initialize the model and prompt
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Store conversation context globally (for simplicity)
context = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global context
    user_input = request.json.get("message")
    
    if user_input.lower() == "exit":
        return jsonify({"response": "Goodbye!"})
    
    # Invoke the chain with the current context and user input
    result = chain.invoke({"context": context, "question": user_input})
    
    # Update the context
    context += f"\nUser: {user_input}\nAI: {result}"
    
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)