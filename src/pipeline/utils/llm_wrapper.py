
import ollama
import os
from pdf2image import convert_from_path
import json

class LlamaResponse():
        def __init__(self,user_data:dict):
            self.ai_reasoning = user_data.get('ai_response')
            self.input_token = user_data.get('input_token')
            self.output_token = user_data.get('output_token')
            self.latency = user_data.get('latency')

def call_llm_model( model_id, doc_url,prompt_text,):

    # conver the docs (.pdf) into the images some models not support direct pdf files hence we have to explicitly convert them into images 
 
    pages = convert_from_path(doc_url, dpi = 200)
    image_path = []
    for i, page in enumerate(pages):
        img_path = f"page_{i}.jpg"
        page.save(img_path,"JPEG")
        image_path.append(img_path)

    response = ollama.chat(
        model = model_id,
        messages  = [{
            "role": "user",
            "content" : prompt_text,
            "images" : image_path
            }],
            format = "json"
            )
    try:
         parsed_output = json.loads(response['message']['content'])
    except json.JSONDecodeError:
         parsed_output = {"error": "Invalid JSON returned", "raw" : response['message']['content']}

    response_data = {
        'ai_response' : parsed_output,
        'input_token' : response.get("prompt_eval_count",0),
        'output_token' : response.get('eval_count',0),
        'latency': response.get('total_duration',0)
    }

    return LlamaResponse(response_data)