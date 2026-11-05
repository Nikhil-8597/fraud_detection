
import ollama
import os
from pdf2image import convert_from_path
import json
import base64
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
from huggingface_hub import InferenceClient
from transformers import pipeline
MODEL = os.getenv("MODEL")
hf_token = os.getenv("HF_TOKEN")

class LlamaResponse():
        def __init__(self,user_data:dict):
            self.ai_reasoning = user_data.get('ai_response')
            self.input_token = user_data.get('input_token')
            self.output_token = user_data.get('output_token')
            self.latency = user_data.get('latency')
            self.function_name = user_data.get('function_name')

def call_llm_model(  doc_url,prompt_text, current_fuction):

    if MODEL == 'llama3.2-vision' :
        print("calling Ollama llama3.2 model ")
        # conver the docs (.pdf) into the images some models not support direct pdf files hence we have to explicitly convert them into images 
        # "images" : image_path
        # pages = convert_from_path(doc_url, dpi = 200)
        # image_path = []
        # for i, page in enumerate(pages):
        #     img_path = f"page_{i}.jpg"
        #     page.save(img_path,"JPEG")
        #     image_path.append(img_path)

        response = ollama.chat(
            model = MODEL,
            messages  = [{
                "role": "user",
                "content" : prompt_text,
            
                }],
                format = "json"
                )
        raw_text = response['message']['content']
        input_tokens = response.get("prompt_eval_count", 0)
        output_tokens = response.get('eval_count', 0)
        latency = response.get('total_duration', 0) / 1e9 # Convert nanoseconds to seconds

    elif MODEL == 'gemma3:4b':
        print("calling Ollama qwen model")
        image_path = '/home/nikhil/nikhil/projects/fraud_detection/data/aadhaarcard.jpeg'
       # Open the file in read-binary ('rb') mode and encode directly
        with open(image_path, "rb") as image_file:
            img_str = base64.b64encode(image_file.read()).decode("utf-8")
            
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    # CRITICAL: Tell the model exactly what JSON keys to generate
                    "content": 'You are Extractor',
                    "images": [img_str]
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            format="json",
            # CRITICAL: Remove repeat_penalty and top_p
            options={
                "temperature": 0.0
            }
        )
        raw_text = response['message']['content']
        input_tokens = response.get("prompt_eval_count", 0)
        output_tokens = response.get('eval_count', 0)
        latency = response.get('total_duration', 0) / 1e9
    else : 

        print("calling HF gemma model")

        

        generator = pipeline(
            "text-generation",
            model="LiquidAI/LFM3-1.7B",
            trust_remote_code=True,
        )

        messages = [{"role": "user", "content": prompt_text}]
        output = generator(
            messages,
            do_sample=True,
            temperature=0.1,
            top_k=50,
            repetition_penalty=1.1,
            max_new_tokens=2048,
        )
        print("Hugging Face Model Output :",output[0]["generated_text"][-1]["content"])
        # client = InferenceClient(
        #     model="meta-llama/Meta-Llama-3.1-8B-Instruct", 
        #     token=hf_token
        # )
        # response = client.chat_completion(
        #     messages=[{"role": "user", "content": "Explain vector databases in one sentence."}],
        #     max_tokens=100
        # )

        # latency = time.time() - start_time
        
        # raw_text = response.choices[0].message.content
        # if response.usage:
        #     input_tokens = response.usage.prompt_tokens
        #     output_tokens = response.usage.completion_tokens

    
    try:
        parsed_output = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed_output = {"error": "Invalid JSON returned", "raw": raw_text}

    response_data = {
        'ai_response': parsed_output,
        'input_token': input_tokens,
        'output_token': output_tokens,
        'latency': latency,
        'function_name': current_fuction
    }

    return LlamaResponse(response_data)