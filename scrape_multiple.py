import requests
from bs4 import BeautifulSoup
from scraper import Scraper

def main():
    categories = []

    main_url = 'https://www.allrecipes.com/recipes/'
    # scrape the list of categories to scrape recipes for
    source = requests.get(main_url).text
    soup = BeautifulSoup(source, 'lxml')
    category_containers = soup.find_all('div', class_='all-categories-col')
    for container in category_containers:
        for section in container.find_all('section'):
            title = section.h3.text
            title = '-'.join(title.lower().split())
            for li in section.ul.find_all('li'):
                cat_name = li.a.text
                cat_name = '-'.join(cat_name.lower().split())
                cat_url = li.a['href']
                categories.append({'title': title, 'category': cat_name, 'url': cat_url})

    # Create a list of scrapers
    max_recipe_num = 30
    for cat in categories:
        scraper = Scraper(cat['title'] + '__' + cat['category'], max_recipe_num=max_recipe_num)
        scraper.get_list_of_categories(cat['url'])
        scraper.parse_category_list_for_recipes()
        scraper.save_to_csv('./data/')


if __name__ == '__main__':
    main()