import itertools
import string
import sys
import os
import psutil
from datetime import datetime

def format_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def calculate_size(length, chars):
    """Calculate combinations and size for a specific length"""
    combinations = len(chars) ** length
    bytes_needed = combinations * (length + 1)  # +1 for newline
    return combinations, bytes_needed

def generate_passwords(length, chars, output_file, max_file_size=1024*1024*1024):  # 1GB default
    """Generate passwords of specific length with file size limit"""
    combinations, total_bytes = calculate_size(length, chars)
    
    # Calculate number of files needed
    num_files = (total_bytes + max_file_size - 1) // max_file_size
    passwords_per_file = combinations // num_files + 1
    
    print(f"\nGenerating {length}-character passwords:")
    print(f"Total combinations: {combinations:,}")
    print(f"Estimated size: {format_size(total_bytes)}")
    print(f"Will be split into {num_files} files")
    
    current_file = 1
    current_count = 0
    f = None
    start_time = datetime.now()
    
    try:
        for combo in itertools.product(chars, repeat=length):
            if current_count % passwords_per_file == 0:
                # Close previous file if open
                if f:
                    f.close()
                # Open new file
                file_name = f"{output_file}.part{current_file}" if num_files > 1 else output_file
                f = open(file_name, 'w', encoding='utf-8')
                print(f"\nWriting to {file_name}")
                current_file += 1
            
            password = ''.join(combo)
            f.write(password + '\n')
            current_count += 1
            
            if current_count % 1000000 == 0:
                progress = (current_count * 100) / combinations
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = current_count / elapsed if elapsed > 0 else 0
                print(f"\rProgress: {progress:.2f}% - {rate:.0f} passwords/sec", end='')
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    finally:
        if f:
            f.close()
    
    print(f"\nCompleted in {datetime.now() - start_time}")

def main():
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    all_chars = lowercase + uppercase + digits + special_chars
    
    print("Character set size:", len(all_chars))
    
    # Get system memory info
    memory = psutil.virtual_memory()
    print(f"Available memory: {format_size(memory.available)}")
    print(f"Total memory: {format_size(memory.total)}")
    
    try:
        length = int(input("Enter password length (1-8 recommended): "))
        if not 1 <= length <= 16:
            raise ValueError("Length must be between 1 and 16")
        
        output_file = input("Enter output filename (default: passwords.txt): ").strip()
        if not output_file:
            output_file = "passwords.txt"
        
        # Calculate size
        combinations, bytes_needed = calculate_size(length, all_chars)
        print(f"\nThis will generate {combinations:,} passwords")
        print(f"Estimated file size: {format_size(bytes_needed)}")
        
        if input("Continue? (y/n): ").lower() != 'y':
            print("Operation cancelled")
            return
        
        # Generate passwords
        generate_passwords(length, all_chars, output_file)
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
