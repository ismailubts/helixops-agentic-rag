import os

def update_env_file():
    """Update .env file to use Google API key instead of OpenAI."""
    env_file = ".env"
    
    if os.path.exists(env_file):
        # Read current content
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace OPENAI_API_KEY with GOOGLE_API_KEY
        if "OPENAI_API_KEY" in content:
            # Extract the API key value (keeping the actual key)
            lines = content.strip().split('\n')
            for line in lines:
                if line.startswith('OPENAI_API_KEY='):
                    api_key = line.split('=', 1)[1]
                    new_content = f"GOOGLE_API_KEY={api_key}"
                    
                    # Write updated content
                    with open(env_file, 'w') as f:
                        f.write(new_content)
                    
                    print("✅ Updated .env file: OPENAI_API_KEY → GOOGLE_API_KEY")
                    return True
        
        print("ℹ️  .env file already contains GOOGLE_API_KEY or no OPENAI_API_KEY found")
        return False
    else:
        # Create new .env file
        with open(env_file, 'w') as f:
            f.write("GOOGLE_API_KEY=your_google_api_key_here")
        
        print("✅ Created new .env file with GOOGLE_API_KEY")
        return True

if __name__ == "__main__":
    update_env_file()
