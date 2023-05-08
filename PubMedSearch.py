import nltk
from Bio import Entrez
import matplotlib.pyplot as plt
import itertools


def search(query):
    Entrez.email = 'h.copoglu@student.han.nl'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax=10000,
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'h.copoglu@student.han.nl'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def groupBy5Year(record):
    return (record['year'] // 5) * 5


def getGroupedRecords(records):
    groupedRecords = []
    for key, group in itertools.groupby(records, groupBy5Year):
        yearRange = f"{key}-{key + 4}"
        titles = [record['title'] for record in group]
        found = False
        for record in groupedRecords:
            if record["year_range"] == yearRange:
                record["titles"].extend(titles)
                found = True
                break
        if not found:
            groupedRecords.append({'year_range': yearRange, 'titles': titles})
    return groupedRecords


if __name__ == '__main__':
    results = search('twin')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    records = []
    for i, paper in enumerate(papers['PubmedArticle']):
        articleTitle = paper['MedlineCitation']['Article']['ArticleTitle']
        issueDate = paper['MedlineCitation']['Article']['Journal'][
            'JournalIssue']['PubDate']['Year']

        issueDict = {'year': int(issueDate), 'title': articleTitle}
        records.append(issueDict)
        print("{}) {} - {}".format(i + 1, articleTitle, issueDate))

    groupedRecords = getGroupedRecords(records)
    groupedRecords = sorted(groupedRecords,
                            key=lambda x: int(x["year_range"].split("-")[0]))

    print(groupedRecords)
    # Extract the number of titles per group
    titles_per_group = [len(rec["titles"]) for rec in groupedRecords]

    # Create a bar plot using matplotlib
    x = [rec["year_range"] for rec in groupedRecords]
    y = titles_per_group
    plt.bar(x, y)

    # Set the x-axis and y-axis labels and title
    plt.xlabel("Year Range")
    plt.ylabel("Number of Titles")
    plt.title("Number of Titles per 5-Year Interval")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Show the plot
    plt.show()
