import urllib.request
import urllib.parse
import json
from pathlib import Path

wiki_articles = {
    'en': ["Earth", "Germany"],
    'de': ["Erde", "Deutschland"]
}

def make_request(title, language="en"):
    url = "https://{}.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={}&explaintext=1&exsectionformat=plain".format(language, urllib.parse.quote(title))
    print("Downloading from {}".format(url))
    response_string = urllib.request.urlopen(url).read()
    response = json.loads(response_string)

    try:
        pages = response['query']['pages']
        for page_num in pages:
            page = pages[page_num]
            text = page['extract']
            return text
        return None
    except e:
        print("Failed to parse json response: {}".format(e))
        return None

def download_files():
    for language in wiki_articles:
        for title in wiki_articles[language]:
            result = make_request(title, language=language)
            if result == None:
                continue

            # create directory
            Path("./data/{}/{}".format(language, title)).mkdir(parents=True, exist_ok=True)

            # write pages
            with open("./data/{}/{}/content.txt".format(language, title), "w", encoding="utf-8") as f:
                f.write(result)
    pass

def main():
    download_files()

if __name__ == "__main__":
    main()