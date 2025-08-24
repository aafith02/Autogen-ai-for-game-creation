import os
import autogen
from autogen import AssistantAgent, UserProxyAgent

# Configuration
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY. Please set it first.")

llm_config = {
    "config_list": [
        {
            "model": "gemini-pro",  # Use the correct model name
            "api_key": API_KEY,
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "api_type": "google",
        }
    ],
    "timeout": 600,
    "temperature": 0,
}

# Agent Definitions
assistant = AssistantAgent(
    name="GameDeveloper",
    llm_config=llm_config,
    system_message="""You are an expert Python game developer. Create complete, 
    working snake game code with pygame. Include:
    - Snake movement controls (arrow keys)
    - Food generation and collision
    - Score tracking
    - Game over detection
    - Restart option
    - Clear instructions"""
)

user_proxy = UserProxyAgent(
    name="GameTester",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config={
        "work_dir": "snake_game",
        "use_docker": False
    }
)

# Task Execution
task = """
Develop a complete Snake game in Python with pygame featuring:
1. Arrow key controls
2. Random food generation
3. Score display
4. Wall/self collision detection
5. Restart functionality
6. Growing snake mechanics

Save as snake_game/main.py with:
- Installation instructions (pip install pygame)
- Running instructions
- Game controls explanation
"""

# Create output directory
os.makedirs("snake_game", exist_ok=True)

# Start development
user_proxy.initiate_chat(assistant, message=task)