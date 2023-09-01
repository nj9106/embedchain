from flask import Flask, jsonify, request

from embedchain import App
from embedchain.config import AppConfig
from embedchain.config import QueryConfig
import sys
import logging

if len(sys.argv) < 2:
    port = 5000
else:
    port = sys.argv[1]

app = Flask(__name__)

appConfig = AppConfig(log_level='DEBUG',collect_metrics=False)
queryConfig = QueryConfig(number_documents=3)
urlPrefix = 'https://www.tapd.cn/31690354/bugtrace/bugs/view?bug_id='

knowledgeConfig = AppConfig(collection_name='knowledge',log_level='DEBUG',collect_metrics=False)
knowledgePrefix  = 'https://helpy-dev.plaso.cn/zh/'
kn_queryConfig = QueryConfig(number_documents=1)

count=0


def initialize_chat_bot():
    global chat_bot
    global knowledge
    chat_bot = App(config=appConfig)
    knowledge = App(config=knowledgeConfig)

# @app.route("/add", methods=["POST"])
# def add():
#     data = request.get_json()
#     data_type = data.get("data_type")
#     url_or_text = data.get("url_or_text")
#     if data_type and url_or_text:
#         try:
#             chat_bot.add(data_type, url_or_text)
#             return jsonify({"data": f"Added {data_type}: {url_or_text}"}), 200
#         except Exception:
#             return jsonify({"error": f"Failed to add {data_type}: {url_or_text}"}), 500
#     return jsonify({"error": "Invalid request. Please provide 'data_type' and 'url_or_text' in JSON format."}), 400


@app.route("/query", methods=["POST"])
def query():
    global count
    data = request.get_json()
    question = data.get("question")
    if question:
        count=count+1
        logging.info(f"---{count}--- {question}")
        try:
            results = chat_bot.retrieve_from_database(question, config=queryConfig)
            out = []
            i = 0
            while i < len(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                o = {"question": results['documents'][0][i], "summary": metadata['summary'], "url": f"{urlPrefix}{metadata['id']}"}
                out.append(o)
                i = i+1
            results = knowledge.retrieve_from_database(question,kn_queryConfig)
            i = 0
            while i < len(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                o = {"question": results['documents'][0][i], "summary": metadata['summary'], "url": f"{knowledgePrefix}{metadata['path']}"}
                out.append(o)
                i = i+1
            logging.info(f"out:{out}")
            return jsonify(out), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "An error occurred. Please try again!"}), 500
    return jsonify({"error": "Invalid request. Please provide 'question' in JSON format."}), 400


# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     question = data.get("question")
#     if question:
#         try:
#             response = chat_bot.chat(question)
#             return jsonify({"data": response}), 200
#         except Exception:
#             return jsonify({"error": "An error occurred. Please try again!"}), 500
#     return jsonify({"error": "Invalid request. Please provide 'question' in JSON format."}), 400


if __name__ == "__main__":
    initialize_chat_bot()
    app.run(host="0.0.0.0", port=port, debug=False)
