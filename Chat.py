from flask import Flask, render_template, request, session
import os
from example import examples
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

app = Flask(__name__)

db = SQLDatabase.from_uri(
    "sqlite:///C:/Users/leo.pickard/Development/DB-Chat/chat.db",
    sample_rows_in_table_info=3
)

contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is. \
Please explicitly state all pieces of information from the chat history in the \
reformulated question that will be needed to understand question completely without \
the chat history as context. Please do not signify in the output that this the question \
has been reformulated. If the user question contains the text 'DATAEXPORT:' you must ensure \
the reformulated question you output starts with the text 'DATAEXPORT:'
"""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

OPENAI_API_KEY = os.environ["ChatKey"]

llm = ChatOpenAI(
    model="gpt-3.5-turbo", temperature=0.0, api_key=OPENAI_API_KEY, verbose=True
)

chat_history = []

contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()


def contextualized_question(input: dict):
    if input.get("chat_history"):
        processed_input = contextualize_q_chain.invoke(
            {
                "chat_history": input["chat_history"],
                "question": input["question"],
            }
        )
        return str(processed_input)
    else:
        return input["question"]


example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(api_key=OPENAI_API_KEY),
    FAISS,
    k=5,
    input_keys=["input"],
)


system_prefix = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know the answer to this question but I can tell you that \
the ultimate answer to the ultimate question of life, the universe, and everything is... 42!" as the answer.

Your final answer must never be cut short, for example if you need to output a list of rows from a set of data you must never cut the \
response short by only displaying the top few rows.

If the user question contains the text 'DATAEXPORT:' you must then return the entire results of the sql query in csv format. csv format \
means you must use a , delimiter and \n as a row terminator. You must always provide a row of columm headings with the csv data.

If the user question does not contain the text 'DATAEXPORT:' you must not use csv format but instead ensure the answers are written clearly \
you can use numbered lists and bullet points where you deem it apropriate.

Here are some examples of user inputs and their corresponding SQL queries:"""

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect"],
    prefix=system_prefix,
    suffix="",
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=full_prompt,
    verbose=True,
    agent_type="openai-tools",
)


def get_completion(prompt):
    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", prompt),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    result = agent.invoke(
        {
            "input": prompt,
            "dialect": "SQLite",
            "agent_scratchpad": [],
        }
    )
    return result["output"]


@app.route("/")
def home():
    return render_template("db_chat.html")


@app.route("/get")
def get_bot_response():
    try:
        userText = request.args.get("msg")
        if not userText:
            error_message = "Error: Message parameter 'msg' is required."
            return error_message.replace("\n", "<br>")

        question = contextualized_question(
            {
                "chat_history": chat_history,
                "question": userText,
            }
        )
        response = get_completion(question)

        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=response))

        output_response = response.replace("\n", "<br>")
        #return question + "<br><br>" + output_response
        return output_response
    except Exception as e:
        error_message = f"Error: An unexpected error occurred. {str(e)}"
        chat_history.append(AIMessage(content=error_message))
        return error_message.replace("\n", "<br>")


@app.route("/info")
def info():
    with open('Create Tables.sql', 'r') as file:
        sql_content = file.read()
    return render_template('info.html', sql_content=sql_content)

@app.route("/faq")
def faq():
    input_elements = [example['input'] for example in examples]
    return render_template('faq.html', input_elements=input_elements)

if __name__ == "__main__":
    app.run()