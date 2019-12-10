"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List

import requests
from requests import get
from bs4 import BeautifulSoup

from env import github_token

def get_titles(soup):
    all_titles = []
    for h3 in soup.find_all("h3"):
        title = h3.text
        all_titles.append(title)
    
    if len(all_titles)>2:
        all_titles = all_titles[2:]
        
    return all_titles

def make_soup():
    start_url = "https://github.com/search?p="
    end_url = "&q=stars%3A%3E100&s=stars&type=Repositories"
    
    collected_titles = []
    
    for page_no in range (1,100):
        url = start_url + str(page_no) + end_url
        headers = {"User-Agent": "Bayes-NLP Project"}
        response = get(url, headers=headers)
    
        soup = BeautifulSoup(response.content, "html.parser")

        title_per_page = get_titles(soup)
        collected_titles.extend(title_per_page)
        
#         if len(title_per_page) == 0:
#             print("---No Titles Found")
#             print(response.text)
            
    #collected_titles = pd.DataFrame({"titles":collected_titles})
    
    return collected_titles

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Replace YOUR_GITHUB_USERNAME below with your github username.
# TODO: Add more repositories to the `repos` list.

repos = make_soup()

repos

headers = {
    "Authorization": f"token {github_token}",
    "User-Agent": "YOUR_GITHUB_USERNAME",
}

if (
    headers["Authorization"] == "token "
    or headers["User-Agent"] == "YOUR_GITHUB_USERNAME"
):
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> requests.Response:
    return requests.get(url, headers=headers)


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    return github_api_request(url).json()["language"]


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    return github_api_request(url).json()


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists
    the files in a repo and returns the url that can be
    used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns
    a dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": requests.get(get_readme_download_url(contents)).text,
    }


def scrape_github_data():
    """
    Loop through all of the repos and process them. Saves the data in
    `data.json`.
    """
    data = [process_repo(repo) for repo in repos]
    json.dump(data, open("data.json", "w"))


if __name__ == "__main__":
    scrape_github_data()