import yaml
import os
from src.pipeline.state.data_state import MyState
from src.pipeline.utils.llm_wrapper import call_llm_model
import inspect

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR,'../utils/prompt_store.yaml')
with open("src/pipeline/utils/prompt_store.yaml", 'r') as file:
    prompt_file = yaml.safe_load(file)

class Nodes():

    #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_MH_10
    def classification_node(self,state:dict) -> dict:
        current_function = inspect.currentframe().f_code.co_name
        """This classification node classify the given document is correct or not."""
        doc_type=state['doc_type']

        yaml_key = f"{doc_type}_prompt"
        classify_prompt = prompt_file.get("classification_prompt",{})
        print(f"classification_prompt: {classify_prompt}")
        underwriting_prompt = classify_prompt.get(yaml_key, '')
        
        print(state)

        # call the llm and pass the document url ( file part) and prompt ( text part)
        underwriting_prompt = "give me any poem of 100 lines"
        response = call_llm_model(state['doc_url'],underwriting_prompt, current_function)
        print(f"Classification_response : {response.ai_reasoning}")
        print(f"Input_Token : {response.input_token}")
        print(f"Output_Token : {response.output_token}")
        print(f"Latency : {response.latency}")
        print(f"Function_Name : {response.function_name}")


        return state

    
    def extraction_node (self, state:dict):
        """This extraction node extract the structured information from the given document"""
        current_function = inspect.currentframe().f_code.co_name
        doc_type = state['doc_type']
        yaml_key = f"{doc_type}_prompt"
        extraction_prompt = prompt_file.get("extraction_prompt",{})
        underwriting_prompt = extraction_prompt.get(yaml_key, '')
        print(f"Extraction_prompt: {underwriting_prompt}")
        print("Extraction_State" , state)
        #response = call_llm_model()
        



        

