from src.pipeline.workflows import graph

def main():
    initial_state = {

        "message" : [],
        "doc_url" : "http://abcd.com/99202901/1234.pdf",
        "prompt" : "",
        "doc_type" : "aadhar"
    }
    print("Start")
    final_state = graph.invoke(initial_state)
    print("End")
    print(f"Final State : {final_state}")



if __name__ == "__main__":
    main()