import yaml
import os
from src.pipeline.state.data_state import MyState
from src.pipeline.utils.llm_wrapper import call_llm_model

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR,'../utils/prompt_store.yaml')
with open("FILE_PATH", 'r') as file:
    prompt_file = yaml.safe_load(file)

class Nodes():

    
    def classification_node(self,state:dict) -> dict:
        """This classification node classify the given document is correct or not."""
        doc_type=state['doc_type']

        yaml_key = f"{doc_type}_prompt"
        classify_prompt = prompt_file.get("classification_prompt",{})
        underwriting_prompt = classify_prompt.get(yaml_key, '')
        
        

        # call the llm and pass the document url ( file part) and prompt ( text part)

        response = call_llm_model()


        return state

    
    def extraction_node (self, state:dict):
        """This extraction node extract the structured information from the given document"""
        doc_type = state['doc_type']
        yaml_key = f"{doc_type}_prompt"
        extraction_prompt = prompt_file.get("extraction_prompt",{})
        underwriting_prompt = extraction_prompt.get(yaml_key, '')
        

        response = call_llm_model()
        



        

