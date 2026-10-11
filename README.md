# go4schools-timetable-api

**One-line Tagline:** A Python-based API to scrape and parse school timetables from Go4Schools.

## Architecture Overview

The `go4schools-timetable-api` repository is structured to automate the process of scraping school timetables from the Go4Schools website. The core components are:

- **sel.py**: This script uses Selenium WebDriver to interact with the Go4Schools login page, authenticate using environment variables for credentials, and extract timetable data.
- **timetable.json**: Stores the extracted timetable data in JSON format.
- **homework.json**: Placeholder for potential future use to store homework-related data.
- **README.md**: This document.

The script (`sel.py`) is designed to run headlessly, making it suitable for automated tasks. It leverages Selenium's capabilities to handle dynamic web content and extract structured timetable information.

## Tech Stack

- **Programming Language:** Python
- **Web Scraping Framework:** Selenium WebDriver
- **Browser Automation:** Firefox (GeckoDriver)
- **Data Handling:** JSON (for storing extracted data)

## Getting Started / Setup Guide

### Prerequisites

1. **Python Installation**: Ensure you have Python 3.x installed on your system.
2. **Selenium WebDriver**: Install Selenium using pip:
   ```bash
   pip install selenium
   ```
3. **GeckoDriver**: Download and set up GeckoDriver for Firefox. Ensure it's in your system's PATH or specify the path in the script.

### Environment Variables

Set the following environment variables to securely store your Go4Schools credentials:

```bash
export USERNAME="your_username"
export PASSWORD="your_password"
```

### Running the Script

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/go4schools-timetable-api.git
   cd go4schools-timetable-api
   ```

2. **Execute the Script**:
   ```bash
   python sel.py
   ```

This will initiate the scraping process, log in to Go4Schools, and save the extracted timetable data into `timetable.json`.

### Notes

- Ensure your network connection is stable during execution.
- The script is designed to run headlessly. If you encounter issues, consider running it without headless mode for debugging purposes.
- The JSON files (`timetable.json` and `homework.json`) are used to store the extracted data. You can modify these files as needed for further processing or integration with other systems.

For any issues or feature requests, please open an issue in the [GitHub repository](https://github.com/yourusername/go4schools-timetable-api).