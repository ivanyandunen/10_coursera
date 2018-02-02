from lxml import etree
import requests
import random
from bs4 import BeautifulSoup
import openpyxl
import os


def get_courses_list():
    courses_list = requests.get(
        'https://www.coursera.org/sitemap~www~courses.xml'
    )
    number_of_links = 20

    xml_tree = etree.fromstring(courses_list.content)
    courses_urls = [child[0].text for child in xml_tree]
    return random.sample(courses_urls, number_of_links)


def get_course_info(url):
    course_html = requests.get(url)
    soup = BeautifulSoup(course_html.content, 'html.parser')
    rating_exists = soup.find('div', class_='ratings-text bt3-visible-xs')
    if rating_exists:
        rating = rating_exists.text
    else:
        rating = 'No rating yet'
    course_info = {
        'Title': soup.h2.text,
        'Language': soup.find('div', class_='rc-Language').text,
        'Start date': soup.find('div', class_='rc-StartDateString').text,
        'Duration(weeks)': len(soup.find_all('div', class_='week')),
        'Rating': rating,
        'Course_url': url
    }
    return course_info


def output_courses_info_to_xlsx(courses_info):
    if os.path.exists('courses_info.xlsx'):
        wb = openpyxl.load_workbook('courses_info.xlsx')
    else:
        wb = openpyxl.Workbook()
    ws = wb.active
    ws.append([
        'Title',
        'Language',
        'Start date',
        'Duration(weeks)',
        'Rating',
        'Course_url'
    ])
    for course in courses_info:
        ws.append([
            course.get('Title'),
            course.get('Language'),
            course.get('Start date'),
            course.get('Duration(weeks)'),
            course.get('Rating'),
            course.get('Course_url')
        ])
    wb.save('courses_info.xlsx')


if __name__ == '__main__':
    courses_info = []
    list_of_courses = get_courses_list()
    for course in list_of_courses:
        courses_info.append(get_course_info(course))
    output_courses_info_to_xlsx(courses_info)
