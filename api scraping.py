import requests
from openpyxl import load_workbook
from openpyxl import Workbook
import time
from requests.exceptions import Timeout

excel = Workbook()
print(excel.sheetnames)
sheet = excel.active
sheet.title = 'Movies'
print(excel.sheetnames)
sheet.append(['University', 'Author', 'Specialization', 'PaperID', 'Title Of Paper', 'Referenced Papers',
              'Title of Referenced Papers', "Author of Referenced paper Name", 'Author of Referenced paper ID', 'Year',
              'Authors Of Paper Name', 'Authors Of Paper Id'])
# Load the workbook and select the active sheet
wb = load_workbook('doctors2.xlsx')
ws = wb.active

# Set the API endpoint and parameters

r = 2

# Loop through each author in the sheet
for row in range(1301, 1401):
    print(row)
    print("//////////////////////////////////////////////////////")

    B = f'A{row}'
    C = f'C{row}'
    D = f'D{row}'

    university = ws[B].value
    author = ws[C].value
    specification = ws[D].value
    LIMIT = [10, 20, 30, 40, 50, 60, 70, 80]
    offset = 0
    A = f'A{r}'
    E = f'B{r}'
    F = f'C{r}'

    sheet[E].value = author
    sheet[A].value = university

    sheet[F].value = specification
    for l in LIMIT:
        limit = l
        # Set the API endpoint and parameters
        url = 'https://api.semanticscholar.org/graph/v1/author/search' + '?offset=' + str(offset) + '&limit=' + str(
            limit)
        params = {
            'query': author,
            'fields': 'papers.title',
            'limit': limit
        }

        # Set the API key header
        headers = {'x-api-key': 'J5stgCYQsu1TAuAxTjqmz72rcyCaOZlUpnu7cyZ0'}
        responses = []

        # Make the API request
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=10, verify=False).json()
                break
            except (Timeout, ConnectionError):
                if attempt == retries - 1:
                    raise
                else:
                    print("Connection error occurred. Retrying...")
                    time.sleep(1)
                    continue
        responses.append(response["data"])
        offset += 10

        if len(responses) >= 1:

            for i in responses:
                if len(i) > 0:

                    papers = i[0]['papers']
                    l = 0
                    while (l < 20) and (l < len(papers)):
                        paper = papers[l]
                        l += 1
                        G = f'D{r}'
                        H = f'E{r}'
                        I = f'F{r}'
                        J = f'G{r}'
                        K = f'H{r}'

                        OriginalpaperID = paper['paperId']
                        title = paper['title']
                        sheet[G].value = OriginalpaperID
                        sheet[H].value = title

                        # Make the API request to get the references for the current paper
                        url = f"https://api.semanticscholar.org/graph/v1/paper/{OriginalpaperID}/references"
                        retries = 3
                        for attempt in range(retries):
                            try:
                                response2 = requests.get(url, headers=headers,
                                                         params={'fields': 'paperId,title,authors'}, timeout=10,
                                                         verify=False).json()
                                break
                            except (Timeout, ConnectionError):
                                if attempt == retries - 1:
                                    raise
                                else:
                                    print("Connection error occurred. Retrying...")
                                    time.sleep(1)
                                    continue
                        data = response2
                        # Loop through each cited paper in the references data
                        p = []
                        t = []
                        an = []
                        if len(data['data']) != 0:
                            for cited_paper in data['data']:

                                authors = cited_paper['citedPaper']['authors']
                                for z in authors:
                                    an.append(z['name'])

                                paperID = cited_paper['citedPaper']["paperId"]
                                Title = cited_paper['citedPaper']["title"]
                                if (paperID != None):

                                    if (len(str(paperID)) == 40):
                                        p.append(paperID)
                                        t.append(Title)

                            # print(paperID)
                            #                 # Insert the data into a new row in the sheet
                            P = f'{p}'.strip('[]')
                            print(P)
                            T = f'{t}'.strip('[]')
                            AN = f'{an}'.strip('[]')

                        if len(t) < 1:
                            continue
                        else:
                            sheet[I].value = P
                            sheet[J].value = T
                            sheet[K].value = AN

                            #             print("///////////////////////////////////////////////////////")

                            # //////////////////////////////////////////////////////////////////////////////////////////////

                            N = f'I{r}'
                            O = f'J{r}'
                            P = f'K{r}'

                            # Set the paper ID of interest

                            # Set the API endpoint URL
                            api_url = f"https://api.semanticscholar.org/graph/v1/paper/{OriginalpaperID}?fields=url,year,authors"

                            # Set the headers for the request
                            headers = {
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
                                "Accept": "application/json",
                                "Accept-Language": "en-US,en;q=0.5",
                                "Connection": "keep-alive",
                                "Referer": "https://www.semanticscholar.org/"
                            }

                            # Set the query parameters for the request
                            params = {
                                "fields": "year,authors"
                            }

                            for attempt in range(retries):
                                try:
                                    response = requests.get(api_url, headers=headers, params=params, timeout=10,
                                                            verify=False).json()
                                    break
                                except (Timeout, ConnectionError):
                                    if attempt == retries - 1:
                                        raise
                                    else:
                                        print("Connection error occurred. Retrying...")
                                        time.sleep(1)
                                        continue
                            # Send a GET request to the API endpoint and retrieve the response as JSON
                            response_json = response

                            # Extract the list of citation objects from the response JSON
                            year = response_json['year']

                            authors = response_json['authors']
                            AU = []
                            ID = []

                            sheet[N].value = year

                            if 'authors' in response_json:
                                for i in authors:
                                    if len(i) > 1:
                                        authorName = i['name']
                                        authorId = i['authorId']
                                        AU.append(authorName)
                                        ID.append(authorId)

                            AAA = f'{AU}'.strip('[]')
                            IDDD = f'{ID}'.strip('[]')
                            sheet[O].value = AAA
                            sheet[P].value = IDDD

                        r += 1


                else:
                    break
        else:
            continue

# # # Save the workbook
excel.save('test34.xlsx')