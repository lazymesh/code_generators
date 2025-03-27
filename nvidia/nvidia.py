import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_keys = ["META_LLMA3_KEY", "DEEPSEEK_R1_LLMA_KEY"]  # we can add more api keys in .env file and add it here
llm_models = ["meta/llama3-70b-instruct", "deepseek-ai/deepseek-r1-distill-llama-8b"] # if more api keys are added then add more models here

# Get API key from environment variables
API_KEY = os.getenv(api_keys[1])
if not API_KEY:
    raise ValueError("NVIDIA_API_KEY not found in environment variables")

def generate_code(prompt, model=llm_models[1]):
    """
    Generate code using NVIDIA AI Foundation Models API.
    
    Args:
        prompt (str): The prompt describing the code you want to generate
        model (str): The model to use for generation
        
    Returns:
        str: The generated code
    """
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,  # Lower temperature for more deterministic code generation
        "top_p": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        result = response.json()
        
        # Extract the generated code from the response
        if "choices" in result and len(result["choices"]) > 0:
            generated_text = result["choices"][0]["message"]["content"]
            return generated_text
        else:
            return "No code was generated."
            
    except requests.exceptions.RequestException as e:
        return f"Error calling NVIDIA API: {str(e)}"
    
# extract code below doesn't work yet so commenting

# def extract_code_blocks(text):
#     """
#     Extract code blocks from markdown-formatted text.
    
#     Args:
#         text (str): Text containing markdown code blocks
        
#     Returns:
#         str: Extracted code without markdown formatting
#     """
#     lines = text.split('\n')
#     code_blocks = []
#     in_code_block = False
#     current_block = []
    
#     for line in lines:
#         if line.strip().startswith('```python'):
#             in_code_block = True
#             continue
#         elif line.strip() == '```' and in_code_block:
#             in_code_block = False
#             code_blocks.append('\n'.join(current_block))
#             current_block = []
#             continue
            
#         if in_code_block:
#             current_block.append(line)
    
#     return '\n\n'.join(code_blocks)

if __name__ == "__main__":
    # Example usage
    prompt = input("Enter a description of the code you want to generate: ")
    
    print("\nGenerating code using NVIDIA AI...\n")
    generated_text = generate_code(prompt)
    
    print("Generated Response:")
    print("-" * 50)
    print(generated_text)
    print("-" * 50)
    
    # Extract just the code blocks
    # code_only = extract_code_blocks(generated_text)
    
    # if code_only:
    #     print("\nExtracted Code:")
    #     print("-" * 50)
    #     print(code_only)
    #     print("-" * 50)
        
    #     # Save the generated code to a file
    #     filename = "generated_code.py"
    #     with open(filename, "w") as f:
    #         f.write(code_only)
    #     print(f"\nCode saved to {filename}")