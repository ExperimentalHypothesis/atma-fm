import requests
from bs4 import BeautifulSoup

def scrap_audio_formats_table() -> list:
    """scrap the table form wiki containing audioformat details"""

    try:
        website = requests.get("https://en.wikipedia.org/wiki/Audio_file_format").text
    except Exception as e:
        print(e)
    else:
        soap = BeautifulSoup(website, "html.parser")
        table_body = soap.find("tbody")
        rows = table_body.find_all("tr")
        
        data = []
        for row in rows:
            cols = row.find_all("td")
            cols_textonly = [i.text.strip() for i in cols]
            if cols_textonly:
                data.append(cols_textonly)
        return data




def parse_audio_extensions(col: list) -> list:
    """parse out only audio extension"""

    extensions = [i[0] for i in col]
    final_list = []

    for i in extensions:
        if " " not in i: 
            final_list.append(i)
        else:
            temp = i.split(", ")
            for i in temp:
                final_list.append(i)
    return final_list


if __name__ == "__main__":
    full_table = scrap_audio_formats_table()
    extensions = set(parse_audio_extensions(full_table))

    print(extensions)
