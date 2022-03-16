import requests
from bs4 import BeautifulSoup



URL = f"https://stackoverflow.com/jobs?q=python&pg="

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = int(pages[-2].get_text(strip = True))
    return last_page

def extract_job(html):
    title = html.find("h2", {"class": "mb4 fc-black-800 fs-body3"}).find("a")["title"]
    company, location = html.find("h3").find_all("span", recursive =  False)
    company = company.get_text(strip = True).strip("-").strip("\r")
    location = location.get_text(strip = True).strip("-").strip("\r")
    # print(location)
    jobid = html["data-jobid"]
    return {"Title": title, "Company": company, "Location": location, "apply_link": f"https://stackoverflow.com/jobs/{jobid}/"}

def extract_jobs(last_page):
    jobs = []
    for page in range (last_page):
        print("scraping so page", (page+1))
        # print(page)
        result = requests.get(f"{URL}{page + 1}")
        # print(result.status_code)
        soup = BeautifulSoup(result.text, "html.parser")
        # print(soup)
        results = soup.find_all("div", {"class": "-job"})
        # print(results)
        for result in results:
            # print(result["data-jobid"])
            job = extract_job(result)
            # print(job)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    # print(last_page)
    # extract_indeed_jobs(20)
    jobs = extract_jobs(last_page)
    return jobs

# get_jobs()
# extract_jobs(get_last_page())