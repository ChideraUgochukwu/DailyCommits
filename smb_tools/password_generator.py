import itertools
import string
import sys
from datetime import datetime

def generate_combinations(min_length=1, max_length=10, output_file="generated_passwords.txt"):
    """
    Generate all possible combinations of characters from min_length to max_length
    and write them to a file.
    """
    # Define character sets
    lowercase = string.ascii_lowercase  # a-z
    uppercase = string.ascii_uppercase  # A-Z
    digits = string.digits  # 0-9
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Combine all characters
    all_chars = lowercase + uppercase + digits + special_chars
    
    # Open file for writing
    with open(output_file, 'w', encoding='utf-8') as f:
        total_combinations = sum(len(all_chars) ** i for i in range(min_length, max_length + 1))
        print(f"Total combinations to generate: {total_combinations:,}")
        print(f"Started at: {datetime.now()}")
        
        # Counter for progress tracking
        current_count = 0
        last_percentage = -1
        
        # Generate combinations for each length
        for length in range(min_length, max_length + 1):
            print(f"\nGenerating {length}-character combinations...")
            
            # Generate combinations using itertools.product
            for combo in itertools.product(all_chars, repeat=length):
                # Join the characters into a string
                password = ''.join(combo)
                
                # Write to file
                f.write(password + '\n')
                
                # Update progress
                current_count += 1
                percentage = (current_count * 100) // total_combinations
                
                if percentage != last_percentage:
                    sys.stdout.write(f"\rProgress: {percentage}% ({current_count:,}/{total_combinations:,})")
                    sys.stdout.flush()
                    last_percentage = percentage
        
        print(f"\n\nCompleted at: {datetime.now()}")
        print(f"Passwords written to: {output_file}")

def main():
    # Get parameters from user
    try:
        min_length = int(input("Enter minimum length (1-10): "))
        max_length = int(input("Enter maximum length (1-10): "))
        output_file = input("Enter output filename (default: generated_passwords.txt): ").strip()
        
        # Validate input
        if not (1 <= min_length <= 10) or not (1 <= max_length <= 10):
            raise ValueError("Lengths must be between 1 and 10")
        if min_length > max_length:
            raise ValueError("Minimum length cannot be greater than maximum length")
        if not output_file:
            output_file = "generated_passwords.txt"
            
        # Calculate approximate file size
        chars = len(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?")
        total_combinations = sum(chars ** i for i in range(min_length, max_length + 1))
        approx_size_bytes = total_combinations * (max_length + 1)  # +1 for newline
        approx_size_gb = approx_size_bytes / (1024**3)
        
        # Warn user about file size
        print(f"\nWarning: The output file will be approximately {approx_size_gb:.2f} GB")
        confirm = input("Do you want to continue? (y/n): ").lower()
        
        if confirm != 'y':
            print("Operation cancelled.")
            return
            
        # Generate combinations
        generate_combinations(min_length, max_length, output_file)
        
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
