import requests
from bs4 import BeautifulSoup
def search_incruit(keyword):
	
	page = 3
	jobs = []

	for i in range(page):
		page = i * 30
		url =f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={page}"

		response = requests.get(url)
		# print(response.content)
		soup = BeautifulSoup(response.text, "html.parser")
		# print(soup.prettify)
		lis = soup.find_all("li", class_="c_col") #li: 태그이름
		# print(lis)
		# print(len(lis))

		for li in lis:
			company = li.find("a", class_="cpname").text
			title = li.find("div",class_ = "cell_mid").find("a").text
			href=li.find("div", class_="cell_mid").find("a").get("href")
			location = li.find("div", class_="cl_md").find_all("span")[0].text
			#print(location)

			job_data = {
			"title" : title,
			"company": company,
			"location": location,
			"href": href
			}

			jobs.append(job_data)

	return jobs