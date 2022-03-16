import requests
from bs4 import BeautifulSoup

def finding_pages(pages, request):
    # data extracted = soup; beautiful soup can understand a lot of things including html
    indeed_soup = BeautifulSoup(request.text, 'html.parser')
    # print(indeed_result.text) # gets html of the website; need to extract info from this html
    # navigating soup datastructure
    # getting page numbers
    pagination = indeed_soup.find("div", {"class": "pagination"})
    # search inside pagination
    # find all anchors ('a')
    links = pagination.find_all("a")
    # print(links)
    # pages = [1]
    temp_spans = []
    # delete last row

    # for link in links:
    #     pages.append(link.find("span").string)

    # if anchor only has one element and that element only has one text --> can call string method on anchor

    # last page number
    # print(links)

    for link in links[:-1]:
        if(link.string is None):
            temp_spans.append((link.string))
        else:
            temp_spans.append(int(link.string))
    if(temp_spans[0] is None):

        return temp_spans[3:]
    else:
        return temp_spans[0:2]

    # print(temp_spans)
    # print(pages)
# indeed_result = requests.get("https://www.indeed.com/jobs?q=python&limit=50&start=250")
LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"
def get_last_page():
    pages = [1]
    prev_length = 1
    # dongle = True
    count = 0
    while(True):
        result = requests.get("https://www.indeed.com/jobs?q=python&limit=50&start={}".format(count*100))
        pages.extend(finding_pages(pages, result))
        if(len(pages) == prev_length):
            # dongle = False
            break
        # print(pages)
        prev_length = len(pages)
        count +=1
        # print(pages)
    # print(pagination)

    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("h2", {"class": "title"})
    # print(title)
    # anchor = title.find("h2", {"class": "title"})
    job_titles = title.find("a")["title"]
    # print(job_titles)
    # find companies

    company = html.find("span", {"class": "company"})
    if company:
        company_anchor = company.find("a")
        # check if company has a link or not
        if company_anchor is not None:
            company = company_anchor.string.strip()
        else:
            company = company.string.strip()
    else:
        company = None

    #extract location
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    job_id = html["data-jk"]
    # print(job_id)
    return {'title': job_titles, 'company': company, "location": location, "link": f"https://www.indeed.com/viewjob?cmp=Codersdata-LLC&t=Data+Scientist&jk={job_id}"}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scraping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")

        # print(result.status_code)

        soup = BeautifulSoup(result.text, 'html.parser')
        #find jobs now
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        # print(results)
        for result in results:
            # print(result)

            job = extract_job(result)
            # print(job)
            jobs.append(job)
            # print(results)
    return jobs

def get_jobs():
    last_page = get_last_page()

    # extract_indeed_jobs(20)
    jobs = extract_jobs(last_page)
    return jobs