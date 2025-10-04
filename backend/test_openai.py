"""
Test OpenAI API connection
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    """Test OpenAI API connection"""
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key (first 10 chars): {api_key[:10]}...")
    
    client = OpenAI(api_key=api_key)
    
    try:
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use a known working model first
            messages=[
                {"role": "user", "content": "Hello, this is a test. Please respond with 'API connection successful'."}
            ],
            max_tokens=50
        )
        
        print("✅ API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        
        # Now test with GPT-5-Codex if available
        try:
            response2 = client.chat.completions.create(
                model="gpt-5-codex",
                messages=[
                    {"role": "user", "content": "Test GPT-5-Codex connection"}
                ],
                max_tokens=50
            )
            print("✅ GPT-5-Codex connection successful!")
            print(f"Response: {response2.choices[0].message.content}")
        except Exception as e:
            print(f"❌ GPT-5-Codex not available: {e}")
            print("Using gpt-4-turbo instead...")
            
            response3 = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "user", "content": "Test GPT-4-Turbo connection"}
                ],
                max_tokens=50
            )
            print("✅ GPT-4-Turbo connection successful!")
            print(f"Response: {response3.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")

if __name__ == "__main__":
    test_openai()
