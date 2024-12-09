# WebSeekly

## Overview

WebSeekly is a tool designed to efficiently search for and organize information related to specific topics.  
By scanning vast amounts of data on the internet, it retrieves and lists only the necessary information based on user-specified topics.

For instance, when searching for "free events" or "latest technology trends," WebSeekly works as follows:

1. **Search Request Submission**  
   The user inputs a topic such as "free events."

2. **Data Exploration**  
   WebSeekly searches for related pages on the internet and collects links.

3. **Information Extraction and Organization**  
   The tool analyzes and extracts only the information relevant to the topic (e.g., "free events") from the collected pages.

4. **Presenting Results**  
   The processed data is presented in a clean list format:

   - Free summer evening concert at XX Station, 7:00 PM (from Official Site A)
   - Free webinar, 3:00 PM (from Official Site B)

---

## Key Features

- Topic-based keyword generation
- Link collection using Google Custom Search API
- Crawling and scraping for event information
- Automated data verification and saving
- Compliance with terms of use and reduced legal risks

---

## Directory Structure

```plaintext
webseekly/
├── pyproject.toml              # Project configuration
├── README.md                   # This file
├── requirements.txt            # Dependency list
├── src/                        # Source code
│   ├── app.py                  # Entry point
│   └── webseekly/              # Main module
│       ├── core/               # Core components
│       │   ├── factory.py
│       │   ├── node.py
│       ├── nodes/              # Individual nodes
│       │   ├── crawl_node.py
│       │   ├── keyword_node.py
│       │   ├── save_node.py
│       │   ├── scrape_node.py
│       │   ├── search_node.py
│       │   ├── verification_node.py
│       └── workflow.py         # Workflow definition
├── test/                       # Test suite
│   ├── test_crawl_node.py
│   ├── test_keyword_node.py
│   ├── test_save_node.py
│   ├── test_scrape_node.py
│   ├── test_search_node.py
│   └── test_verification_node.py
└── uv.lock                     # Lock file for virtual environment
```

## Setup

### Requirements

- Python 3.10 or higher
- Google Custom Search API keys (configuration details below)

### Installation

1. Clone the repository:

   ```plaintext
   git clone https://github.com/username/webseekly.git
   cd webseekly
   ```

2. Create and activate a virtual environment:

   ```plaintext
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```plaintext
   pip install -r requirements.txt
   ```

4. Create a .env file and configure API keys

5. Start the application:
   ```plaintext
   python src/app.py
   ```

## Usage

1. Enter a topic (e.g., "free events," "online").
2. WebSeekly automatically performs the following processes:
Generates relevant keywords
Searches for and collects related links
Scrapes and verifies the information
3. Retrieve the desired event information in a clean list format.

---

## Testing

Run the test suite to verify that each node functions correctly:
   ```plaintext
   pytest test/
   ```
# API Key Setup

## Google Custom Search API

1. Visit the Google Cloud Console.
2. Create a project and enable the Custom Search JSON API.
3. Obtain an API key and configure it in your .env file.

   ```plaintext
   GOOGLE_CUSTOM_SEARCH_API_KEY=your_api_key_here
   GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id_here
   ```

## OpenAI API

1. Visit OpenAI's API platform.
2. Sign up or log in and obtain an API key.
3. Add the key to your .env file:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```

---

# Notes
- API keys are essential for this project and must be configured in a .env file.
- WebSeekly is designed to comply with terms of service and respects robots.txt directives, ensuring responsible scraping practices.


---

# License

This project is licensed under the MIT License.

MIT License
Copyright (c) 2024 genga6
