#initialization of connection to the LLM
#note if you want  to test this yourself you will need to create a .env on your branch and setup your .env for API key security
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


#loads api key
load_dotenv()

#initializes gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

#test function to send input into llm and get a response
def ask_llm(prompt):
    response = llm.invoke(prompt)
    return response.content


#tesing the LLM function
if __name__ == "__main__":
    print(ask_llm("this is a test please respond"))
