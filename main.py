import requests
from bs4 import BeautifulSoup
import pandas as pd
from icecream import ic

def ReadPage(url):
    # Make a request to the website
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the second table on the page
    tables = soup.find_all('table')
    second_table = tables[1]  # Assuming the second table, adjust the index if needed

    # Initialize empty lists for data
    data_list = []

    # Loop through rows in the second table
    for j, row in enumerate(second_table.find_all('tr')):
        # Skips first
        if j == 0:
            continue

        # Initialize an empty dictionary for each row
        row_data = {}

        # Loop through cells in the row
        for i, cell in enumerate(row.find_all('td')):
            # Check if the cell contains an image
            img_tag = cell.find('img')

            if img_tag:
                img_alt = img_tag.get('alt', '')
                if img_alt == "Official":
                    img_alt = ""
                row_data[f'column{i + 1}'] = img_alt
            else:
                cellText = cell.get_text(strip=True)
                if cellText == "OP":
                    cellText = ""
                row_data[f'column{i + 1}'] = cellText

        # Add the row data to the list
        data_list.append(row_data)

    # Create a Pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    df = df.fillna('')
    df.columns = ["Champion", "Top", "Jungle", "Mid", "Bot", "Support", "Undefined"]
    roleList = ["Top", "Jungle", "Mid", "Bot", "Support", "Undefined"]
    champDict = {}
    for index, row in df.iterrows():
        ic(row)
        champName = row["Champion"]
        champsRole = []
        for role in roleList:
            if row[role] == "Yes":
                champsRole.append(role)
        champDict.update({champName:champsRole})

    df = pd.DataFrame(list(champDict.items()), columns=['Champion', 'Roles'])

    return df

def main():
    ParseURL = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'
    champFrame = ReadPage(ParseURL)
    ic(champFrame)
    champFrame.to_csv('Champs.csv', index=False)

if __name__ == "__main__":
    main()