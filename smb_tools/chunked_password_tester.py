import itertools
import string
import subprocess
import os
import random
from datetime import datetime
import time

class PasswordChunkGenerator:
    def __init__(self, chunk_size=100000, length=8):
        self.chunk_size = chunk_size
        self.length = length
        self.chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.used_passwords = set()
        self.current_chunk = set()
        
        # Create or load progress file
        self.progress_file = "generator_progress.txt"
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                self.used_passwords = set(f.read().splitlines())
        
        print(f"Initialized with {len(self.used_passwords)} previously tested passwords")
    
    def generate_random_password(self):
        """Generate a random password of specified length"""
        return ''.join(random.choices(self.chars, k=self.length))
    
    def generate_chunk(self):
        """Generate a new chunk of unique passwords"""
        self.current_chunk.clear()
        print(f"\nGenerating chunk of {self.chunk_size} passwords...")
        start_time = time.time()
        
        while len(self.current_chunk) < self.chunk_size:
            password = self.generate_random_password()
            if password not in self.used_passwords and password not in self.current_chunk:
                self.current_chunk.add(password)
            
            if len(self.current_chunk) % 10000 == 0 and len(self.current_chunk) > 0:
                print(f"\rGenerated: {len(self.current_chunk)}/{self.chunk_size}", end='')
        
        print(f"\nChunk generated in {time.time() - start_time:.2f} seconds")
        
        # Write chunk to file
        with open("current_chunk.txt", 'w') as f:
            for password in self.current_chunk:
                f.write(password + '\n')
        
        # Update used passwords
        self.used_passwords.update(self.current_chunk)
        
        # Save progress
        with open(self.progress_file, 'a') as f:
            for password in self.current_chunk:
                f.write(password + '\n')
    
    def clear_current_chunk(self):
        """Clear the current chunk file"""
        if os.path.exists("current_chunk.txt"):
            os.remove("current_chunk.txt")

def run_smb_test():
    """Run the SMB testing script and check for success"""
    print("\nStarting SMB test...")
    result = subprocess.run(['smb_chunked.bat'], capture_output=True, text=True)
    
    # Check if password was found
    if os.path.exists("password_found.txt"):
        with open("password_found.txt", 'r') as f:
            password = f.read().strip()
        print(f"\nSUCCESS! Password found: {password}")
        return True
    return False

def main():
    # Initialize generator
    chunk_size = 100000
    generator = PasswordChunkGenerator(chunk_size=chunk_size)
    
    try:
        chunk_count = 0
        start_time = datetime.now()
        
        while True:
            chunk_count += 1
            print(f"\nProcessing chunk #{chunk_count}")
            print(f"Total passwords tested: {len(generator.used_passwords)}")
            print(f"Running time: {datetime.now() - start_time}")
            
            # Generate new chunk
            generator.generate_chunk()
            
            # Run SMB test
            if run_smb_test():
                break
            
            # Clear chunk file
            generator.clear_current_chunk()
            
            # Optional delay between chunks
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Cleanup
        generator.clear_current_chunk()
        print("\nFinal Statistics:")
        print(f"Total chunks processed: {chunk_count}")
        print(f"Total passwords tested: {len(generator.used_passwords)}")
        print(f"Total running time: {datetime.now() - start_time}")

if __name__ == "__main__":
    main()
