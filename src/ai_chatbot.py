#!/usr/bin/env python3
"""
Simple AI Chatbot with Multi-Provider Support
Supports GitHub Models, Anthropic Claude, and Google Gemini
"""

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import AI orchestrator
try:
    from services.ai_orchestrator import AIOrchestrator, TaskType
    ORCHESTRATOR_AVAILABLE = True
except ImportError:
    ORCHESTRATOR_AVAILABLE = False
    print("⚠️  AI Orchestrator not available. Using GitHub Models only.")

class AIChatbot:
    def __init__(self, use_orchestrator=True):
        """
        Initialize the chatbot with multi-provider support
        
        Args:
            use_orchestrator: If True, use AI orchestrator for intelligent provider selection
        """
        self.use_orchestrator = use_orchestrator and ORCHESTRATOR_AVAILABLE
        
        # Initialize GitHub Models as primary/fallback
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
        
        # Initialize OpenAI client for GitHub Models
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
        
        # Initialize AI orchestrator if available
        if self.use_orchestrator:
            try:
                self.orchestrator = AIOrchestrator(primary_provider="github")
                print("✅ AI Orchestrator initialized with multiple providers")
                self._show_available_providers()
            except Exception as e:
                print(f"⚠️  Could not initialize orchestrator: {e}")
                self.use_orchestrator = False
        
        # System message to define chatbot personality
        self.system_message = {
            "role": "system",
            "content": """You are a helpful, friendly AI assistant. You provide clear, 
            concise, and accurate responses. You're knowledgeable about various topics 
            and always try to be helpful while maintaining a conversational tone."""
        }
        
        # Store conversation history
        self.conversation_history = [self.system_message]
    
    def _show_available_providers(self):
        """Show available AI providers"""
        if not self.use_orchestrator:
            return
        
        try:
            providers = self.orchestrator.get_available_providers()
            if providers:
                print("🤖 Available AI Providers:")
                for provider in providers:
                    status_icon = "✅" if provider.get("status") == "available" else "❌"
                    name = provider.get("provider", provider.get("name", "Unknown"))
                    print(f"   {status_icon} {name}")
        except Exception as e:
            print(f"   ⚠️  Could not check providers: {e}")
    
    def get_response(self, user_input):
        """Get response from the AI model with intelligent provider selection"""
        try:
            # Add user message to conversation history
            user_message = {"role": "user", "content": user_input}
            self.conversation_history.append(user_message)
            
            # Try to use orchestrator first
            if self.use_orchestrator:
                try:
                    result = self.orchestrator.get_response(
                        messages=self.conversation_history,
                        system_prompt=self.system_message["content"],
                        temperature=0.7
                    )
                    
                    assistant_response = result["content"]
                    provider = result.get("provider", "unknown")
                    
                    # Add metadata to track which provider was used
                    print(f"  [via {provider}]", end=" ", flush=True)
                    
                    # Add assistant response to conversation history
                    assistant_message = {"role": "assistant", "content": assistant_response}
                    self.conversation_history.append(assistant_message)
                    
                    return assistant_response
                    
                except Exception as e:
                    print(f"  [orchestrator failed: {e}, falling back to GitHub]", flush=True)
                    # Fall through to GitHub Models
            
            # Fallback to GitHub Models
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
🔄 /providers - Show available AI providers
❓ /help - Show this help message  
🚪 /quit or /exit - Exit the chatbot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        print(help_text)
    
    def show_providers(self):
        """Show detailed information about available providers"""
        if not self.use_orchestrator:
            print("🤖 Current Provider: GitHub Models")
            print("   Model:", self.model)
            return
        
        try:
            providers = self.orchestrator.get_available_providers()
            print("\n🤖 Available AI Providers:")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for provider in providers:
                status_icon = "✅" if provider.get("status") == "available" else "❌"
                name = provider.get("provider", provider.get("name", "Unknown"))
                model = provider.get("model", "N/A")
                description = provider.get("description", "")
                best_for = provider.get("best_for", [])
                
                print(f"\n{status_icon} {name}")
                print(f"   Model: {model}")
                if description:
                    print(f"   Description: {description}")
                if best_for:
                    print(f"   Best for: {', '.join(best_for)}")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        except Exception as e:
            print(f"⚠️  Could not retrieve provider information: {e}")
    
    def run(self):
        """Main chatbot loop"""
        print("🤖 AI Chatbot Started!")
        if self.use_orchestrator:
            print("💡 Multi-Provider Mode: Intelligent routing enabled")
        else:
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
                elif user_input.lower() == '/providers':
                    self.show_providers()
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