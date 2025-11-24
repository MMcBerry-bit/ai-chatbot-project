#!/usr/bin/env python3
"""
Simple AI Chatbot using GitHub Models
"""

import os
import sys
from openai import OpenAI

class AIChatbot:
    def __init__(self):
        """Initialize the chatbot with GitHub model configuration"""
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4.1-mini"  # Fast, efficient model
        
        # Get GitHub token from environment variable
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            print("❌ Error: GITHUB_TOKEN environment variable is required!")
            print("📝 Please set your GitHub Personal Access Token:")
            print("   1. Go to https://github.com/settings/tokens")
            print("   2. Generate a new token with appropriate permissions")
            print("   3. Set it as environment variable: set GITHUB_TOKEN=your_token_here")
            sys.exit(1)
        
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
        
        # System message to define chatbot personality
        self.system_message = {
            "role": "system",
            "content": """You are a helpful, friendly AI assistant. You provide clear, 
            concise, and accurate responses. You're knowledgeable about various topics 
            and always try to be helpful while maintaining a conversational tone."""
        }
        
        # Store conversation history
        self.conversation_history = [self.system_message]
        
    def get_response(self, user_input):
        """Get response from the AI model"""
        try:
            # Add user message to conversation history
            user_message = {"role": "user", "content": user_input}
            self.conversation_history.append(user_message)
            
            # Get response from the model
            response = self.client.chat.completions.create(
                messages=self.conversation_history,
                temperature=0.7,  # Balanced creativity
                top_p=0.95,
                max_tokens=500,   # Reasonable response length
                model=self.model
            )
            
            # Extract the assistant's response
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to conversation history
            assistant_message = {"role": "assistant", "content": assistant_response}
            self.conversation_history.append(assistant_message)
            
            return assistant_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history but keep system message"""
        self.conversation_history = [self.system_message]
        print("🧹 Conversation history cleared!")
    
    def show_help(self):
        """Show available commands"""
        help_text = """
🤖 AI Chatbot Commands:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Just type your message and press Enter
🧹 /clear - Clear conversation history
❓ /help - Show this help message  
🚪 /quit or /exit - Exit the chatbot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        print(help_text)
    
    def run(self):
        """Main chatbot loop"""
        print("🤖 AI Chatbot Started!")
        print("💡 Using model:", self.model)
        print("🔗 GitHub Models endpoint")
        self.show_help()
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['/quit', '/exit']:
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                elif user_input.lower() == '/clear':
                    self.clear_history()
                    continue
                elif user_input.lower() == '/help':
                    self.show_help()
                    continue
                
                # Get and display AI response
                print("🤖 Assistant: ", end="", flush=True)
                response = self.get_response(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again or type /quit to exit.")

def main():
    """Main function to run the chatbot"""
    chatbot = AIChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()