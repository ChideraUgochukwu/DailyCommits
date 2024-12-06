import string

def calculate_size():
    # Character set
    lowercase = string.ascii_lowercase  # 26 chars
    uppercase = string.ascii_uppercase  # 26 chars
    digits = string.digits  # 10 chars
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # 23 chars
    
    all_chars = len(lowercase + uppercase + digits + special_chars)
    print(f"Total unique characters: {all_chars}")
    
    total_combinations = 0
    total_bytes = 0
    
    for length in range(1, 9):
        combinations = all_chars ** length
        bytes_per_line = length + 1  # +1 for newline character
        total_bytes_this_length = combinations * bytes_per_line
        
        total_combinations += combinations
        total_bytes += total_bytes_this_length
        
        print(f"\nLength {length}:")
        print(f"Combinations: {combinations:,}")
        print(f"Bytes needed: {total_bytes_this_length:,}")
        
    print(f"\nTotal combinations: {total_combinations:,}")
    print(f"Total file size: {total_bytes:,} bytes")
    print(f"Total file size: {total_bytes/1024/1024/1024:.2f} GB")

if __name__ == "__main__":
    calculate_size()
