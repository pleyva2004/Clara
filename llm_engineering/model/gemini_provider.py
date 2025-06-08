import os
from pathlib import Path
from typing import Optional, List

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig, Tool, FunctionDeclaration



class GeminiClient:
    def __init__(self):
        # Get the project root directory (3 levels up from this file)
        project_root = Path(__file__).parent.parent.parent
        # Load the .env file from the project root
        load_dotenv(project_root / '.env')
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
    
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, 
                     temperature: float = 0.7, top_p: float = 0.95, 
                     top_k: int = 40, tools: Optional[List[dict]] = None) -> str:
        config = GenerateContentConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k
        )
        
        if tools:
            # Convert dict to Tool objects
            tool_objects = []
            for tool_dict in tools:
                if "function_declarations" in tool_dict:
                    func_decls = []
                    for func_decl in tool_dict["function_declarations"]:
                        func_decls.append(FunctionDeclaration(**func_decl))
                    tool_objects.append(Tool(function_declarations=func_decls))
            config.tools = tool_objects
            
        if system_instruction:
            config.system_instruction = system_instruction
            
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=config
        )
        return response.text if response.text else ""
    
    def close(self):
        """
        Close the Gemini client session and clean up resources.
        """
        # The Google Generative AI client doesn't require explicit cleanup
        # but we'll keep this method for consistency and future-proofing
        pass 