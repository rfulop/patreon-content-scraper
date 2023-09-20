<div align="center">

<h3 align="center">Patreon Content Scraper</h3>

  <p align="center">
    A Patreon API manager for retrieving Patreon campaigns you are subscribed to.
    <br />
    <br />
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

The **Patreon Content Scraper** is a Python tool designed to help you retrieve content from campaigns you are subscribed to on Patreon. 
It simplifies the process of organizing and saving content from your favorite creators. With this tool, you can structure your Patreon content by placing each campaign in its own folder and categorizing each post within its respective campaign folder.

### What it does
- Retrieves all campaigns you are subscribed to
- Retrieves all posts from each campaign
- Retrieves all attachments from each post
- Organizes all content in a folder structure
- Categorizes each post within its respective campaign folder
- Downloads all attachments to their respective post folder


### Built With

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

To use this software, you'll need Python3.6 or higher installed on your system. You can download the latest version of Python [here](https://www.python.org/downloads/).

### Installation

1. Clone the repository:
```sh
git clone https://github.com/rfulop/patreon-content-scraper.git
```

2. Navigate to the project directory:
```sh
cd patreon-content-scraper
```
   
3. Create a virtual environment:
```sh
python3 -m venv venv
```
   
4. Activate the virtual environment:
    * On Windows:
   ```sh
    venv\Scripts\activate.bat
   ```
    * On Linux or MacOS:
   ```sh
   source venv/bin/activate
   ```

5. Install the required packages:
```sh
pip install -r requirements.txt
```

6. Update `.env` file with your Patreon credentials

7. Run the program to start scraping all campaign you are subscribed to:
```sh
python3 main.py
```



<!-- USAGE EXAMPLES -->
## Usage

By default, the program will scrape all campaigns you are subscribed to.
```sh
python3 main.py
```


You can also use this tool to scrape a single campaign:
    
``` python
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
campaign_id = ""

patreon_manager = PatreonManager(email, password)
if patreon_manager.login():
   patreon_manager.scrape_campaign(campaign_id)
```

<!-- NOTES -->
## Notes

 - Please be aware that the code in this project has been tested in a limited number of scenarios and environments. There may be undiscovered issues or unhandled edge cases. Use this software at your own discretion and consider contributing to its improvement if you encounter any problems.  
Feel free to report any issues, bugs, or improvements through the [Issues](https://github.com/rfulop/patreon-content-scraper/issues) section.
  

 - This script is provided for educational and personal automation purposes. Be sure to abide by Patreon's terms of use when using this tool. Please be aware to not publish your Patreon credentials located in the `.env` file.
  

 - Login credentials (email address and password) are stored locally on your system and are not shared or published.


<!-- Author -->
## Author
- [rfulop](https://github.com/rfulop)


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.




