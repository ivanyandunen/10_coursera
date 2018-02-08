from lxml import etree
import requests
import random
from bs4 import BeautifulSoup
import openpyxl
import os
import argparse


def get_random_courses_urls(site_content):
    number_of_links = 20

    xml_tree = etree.fromstring(site_content.content)
    courses_urls = [child[0].text for child in xml_tree]
    return random.sample(courses_urls, number_of_links)


def get_course_info(url, course_html):
    soup = BeautifulSoup(course_html.content, 'html.parser')
    rating_exists = soup.find('div', class_='ratings-text bt3-visible-xs')
    if rating_exists:
        rating = rating_exists.text
    else:
        rating = rating_exists
    course_info = {
        'Title': soup.h2.text,
        'Language': soup.find('div', class_='rc-Language').text,
        'Start date': soup.find('div', class_='rc-StartDateString').text,
        'Duration(weeks)': len(soup.find_all('div', class_='week')),
        'Rating': rating,
        'Course_url': url
    }
    return course_info


def output_courses_info_to_xlsx(path_to_file, courses_info):
    if os.path.exists(path_to_file):
        return None
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
            course['Title'],
            course['Language'],
            course['Start date'],
            course['Duration(weeks)'],
            course['Rating'],
            course['Course_url']
        ])
    return wb


def get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--outfile',
        help='Path to xlsx file with information about courses. '
             'Without it file will be saved to current directory'
             ' as courses_info.xlsx',
        default='courses_list.xlsx'
    )
    return parser.parse_args()


def get_path_to_save_file(outfile):
    default = 'courses_list.xlsx'
    if outfile and os.path.isdir(outfile):
        print('The path you specified is a directory. '
              'File will be saved in current location')
        return default
    elif outfile:
        return outfile


if __name__ == '__main__':
    args = get_parser_args()
    site_content = requests.get(
        'https://www.coursera.org/sitemap~www~courses.xml'
    )
    courses_info = []
    path_to_file = get_path_to_save_file(args.outfile)
    print(path_to_file)
    courses_urls = get_random_courses_urls(site_content)
    for course_url in courses_urls:
        course_html = requests.get(course_url)
        courses_info.append(get_course_info(course_url, course_html))
    courses_workbook = output_courses_info_to_xlsx(path_to_file, courses_info)
    if not courses_workbook:
        print('File exists. Please enter a new one')
    else:
        courses_workbook.save(path_to_file)

