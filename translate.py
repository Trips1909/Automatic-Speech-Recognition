# to be sent
from django.http import JsonResponse
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI,AzureChatOpenAI
from langchain.memory import ConversationBufferMemory,ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
import regex as re
from langchain.chains import ConversationChain
# from dotenv import load_dotenv
import os

OPENAI_API_KEY="aaaf10717998437a8bf94efe5b9081fb"
OPENAI_API_BASE="https://ey-sandbox-we.openai.azure.com/"
OPENAI_API_TYPE="azure"
OPENAI_API_VERSION="2023-07-01-preview"
os.environ["OPENAI_API_TYPE"] =OPENAI_API_KEY
os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def get_conversation_chain():
    llm = AzureChatOpenAI(deployment_name="gpt-35-turbo",temperature=0,top_p  = 0.6,presence_penalty = 0.3)
    # memory = ConversationKGMemory(llm=llm, return_messages=True)

    conversation = ConversationChain(
    llm=llm, 
    verbose=False, 
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm)
    )

    return conversation


def refine_translation(context):
    pattern = r'#start(.*?)#End'
    matches = re.search(pattern, context, re.DOTALL)
    if matches:
        extracted_text = matches.group(1)
        return extracted_text.strip()
    else:
        print("No match found")
        return ""
    
def refine_transliteration(context):
    pattern = r'#start_tr(.*?)#End_tr'
    matches = re.search(pattern, context, re.DOTALL)
    if matches:
        extracted_text = matches.group(1)
        return extracted_text.strip()
    else:
        print("No match found")
        return ""

translate_prompt = """
Translate the following context: {}
in {} language, also keep the language script as identified.
remember to always start the translated part which is in different language with #start and end it with #End
"""

engliteral_prompt = """
For the given context: {}
can you please transliterate it in english literal keeping the pheontic same as the language.
remember to always start the transliterated part #start_tr and end it with #End_tr
"""


def translate_llm(chainc,chunk,lang):
    translated_text = chainc.predict(input = translate_prompt.format(chunk,lang))
    translated_text = refine_translation(translated_text)
    print("translated part -----------",translated_text)
    transliterated_text = chainc.predict(input = engliteral_prompt.format(translated_text))
    transliterated_text = refine_transliteration(transliterated_text)
    print("transliterated part -----------",transliterated_text)
    return translated_text,transliterated_text

# # test
# def trans_main(text):
#     chain = get_conversation_chain()
#     return(translate_llm(chain,text,"hindi"))

#test
def trans_main(text, language):
    chain = get_conversation_chain()
    return translate_llm(chain, text, language)
