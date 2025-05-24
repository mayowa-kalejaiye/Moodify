import random
import string
import os

def generate_secret_key(length=50):
    """Generate a secure random string for Django's SECRET_KEY setting."""
    chars = string.ascii_letters + string.digits + string.punctuation
    # Remove characters that might cause issues in .env file
    chars = chars.replace("'", "").replace('"', "").replace('\\', "")
    return ''.join(random.choice(chars) for _ in range(length))

if __name__ == "__main__":
    # Generate a new secret key
    new_key = generate_secret_key()
    print("\nGenerated new Django SECRET_KEY:")
    print(new_key)
    
    # Create/update .env file
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    
    # Update the secret key
    env_vars['DJANGO_SECRET_KEY'] = new_key
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
        
        # Add default values if they don't exist
        if 'DEBUG' not in env_vars:
            f.write("DEBUG=True\n")
        if 'ALLOWED_HOSTS' not in env_vars:
            f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
    
    print(f"\nSecret key has been saved to {env_file}")
    print("IMPORTANT: Add .env to your .gitignore file if you haven't already!")
