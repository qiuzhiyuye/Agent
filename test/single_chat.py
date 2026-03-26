import sys
import os

# Add the parent directory to sys.path to allow importing agent modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from agent.llm import call_llm

def main():
    # Ask once (prompt user for input)
    try:
        user_input = input("请输入您的问题: ")
    except EOFError:
        return

    if not user_input.strip():
        print("未输入内容。")
        return

    print(f"\n正在询问大模型: {user_input}\n")
    
    # Call the LLM with the input content
    # call_llm with just 'prompt' returns a string response
    response = call_llm(prompt=user_input)
    
    print("-" * 20)
    print("大模型回复:")
    print(response)
    print("-" * 20)

if __name__ == "__main__":
    main()
