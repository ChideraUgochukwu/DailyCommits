# SMB Password Testing Suite

## Overview
A sophisticated password testing system designed for SMB (Server Message Block) authentication. This project implements an efficient, memory-conscious approach to password testing by generating and testing passwords in manageable chunks.

## ⚠️ Important Notice
This tool is intended for **legitimate security testing only**. Using this tool without explicit permission from the system owner may be illegal. Always ensure you have proper authorization before conducting any security testing.

## 🔑 Key Features

### Memory Efficient Design
- Generates passwords in chunks of 100,000
- Minimizes memory usage through chunk-based processing
- Cleans up resources between attempts
- Prevents duplicate password testing

### Robust Progress Tracking
- Saves progress after each chunk
- Maintains record of tested passwords
- Supports session resumption
- Tracks total attempts and runtime

### Smart Credential Management
- Saves previously used credentials
- Option to reuse or update saved credentials
- Secure credential handling

## 📁 Project Structure

### Core Components

1. `smb_chunked.bat`
   - Main SMB testing script
   - Handles network connections
   - Manages authentication attempts
   - Tracks progress and results

2. `chunked_password_tester.py`
   - Password generation engine
   - Chunk management system
   - Progress tracking and resumption
   - Resource cleanup

### Support Files

1. `smb_creds.txt`
   - Stores saved credentials
   - Format: IP=x.x.x.x, USERNAME=user

2. `current_chunk.txt`
   - Contains current password chunk
   - Automatically managed by the system
   - Cleaned between chunks

3. `generator_progress.txt`
   - Tracks tested passwords
   - Prevents duplicates
   - Enables session resumption

4. `attempt_counter.txt`
   - Maintains total attempt count
   - Persists between sessions

5. `password_found.txt`
   - Created when successful
   - Contains the working password

## 🛠️ Technical Details

### Password Generation
- Character set: Letters (a-z, A-Z), Numbers (0-9), Special characters
- Password length: 8 characters
- Unique password generation
- Random distribution

### Memory Management
- Chunk size: 100,000 passwords
- Active memory usage: ~10MB per chunk
- Disk usage: ~1MB per chunk file
- Efficient cleanup routines

### Network Handling
- Automatic connection cleanup
- Error handling for network issues
- Connection timeout management
- Session management

## 📋 Prerequisites
- Windows operating system
- Python 3.6 or higher
- Network access to target system
- Administrative privileges (for SMB testing)
- Sufficient disk space (~100MB recommended)

## 🚀 Installation

1. Clone or download the project files
2. Ensure Python is installed and in PATH
3. Required Python packages:
   ```
   pip install psutil
   ```

## 💻 Usage

### Basic Usage
1. Open command prompt in project directory
2. Run the main script:
   ```
   python chunked_password_tester.py
   ```
3. Follow the prompts for credentials

### Command Line Options
- First run: Enter IP and username
- Subsequent runs: Option to reuse credentials

### Progress Monitoring
- Real-time attempt counting
- Chunk generation progress
- Network connection status
- Success/failure feedback

## 🔄 Recovery and Resume

### Automatic Recovery
- Script can be safely interrupted
- Progress automatically saved
- Resumes from last attempt
- Maintains password history

### Manual Recovery
1. Check `generator_progress.txt` for progress
2. Verify `attempt_counter.txt` for count
3. Delete corrupted chunks if necessary
4. Restart script to resume

## 🔍 Troubleshooting

### Common Issues
1. Network Connection Failures
   - Verify network connectivity
   - Check IP address
   - Confirm SMB port accessibility

2. Permission Issues
   - Verify administrative rights
   - Check username format
   - Confirm account permissions

3. Resource Issues
   - Ensure sufficient disk space
   - Check available memory
   - Monitor system resources

### Error Messages
- "Connection failed": Network/credential issue
- "Access denied": Permission problem
- "Resource busy": SMB connection issue

## 📊 Performance

### Typical Performance Metrics
- Password generation: ~10,000/second
- Testing speed: ~1-2 passwords/second
- Disk usage: ~100MB maximum
- Memory usage: ~50MB maximum

### Optimization Tips
1. Adjust chunk size for system
2. Monitor network latency
3. Balance speed vs. resource usage
4. Consider system limitations

## 🔒 Security Considerations

### Best Practices
1. Use only on authorized systems
2. Maintain secure credential storage
3. Clear sensitive files after use
4. Monitor system access logs

### Data Protection
1. Credentials stored locally
2. Progress files contain no sensitive data
3. Temporary files automatically cleaned
4. Secure failure handling

## 📝 Logging and Monitoring

### Log Files
- Progress tracking in real-time
- Attempt counting
- Success/failure logging
- Session information

### Monitoring Features
- Real-time progress display
- Resource usage tracking
- Error reporting
- Success notification

## 🤝 Contributing
Contributions are welcome! Please ensure:
1. Code follows existing style
2. All tests pass
3. Documentation is updated
4. Security best practices are followed

## 📜 License
This project is for educational and authorized testing purposes only.

## 📞 Support
For issues and questions:
1. Check troubleshooting guide
2. Review error messages
3. Verify system requirements
4. Check network connectivity

## 🔄 Version History
- v1.0: Initial release
- v1.1: Added progress tracking
- v1.2: Improved memory management
- v1.3: Enhanced error handling

Remember: Always use this tool responsibly and legally!
