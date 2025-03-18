from bs4 import BeautifulSoup
import requests
import lxml
import os

from utils.filework import write_img_to_file
from utils.validation.db_validation import validated_teacher_name

class Parser:
    def __init__(self, url, group=""):
        self.__url = url
        self.__group = group
        self.__error_code = 0
        
    
    def __set_page_group(self):
        self.__url += f"{self.__group}/?week=all&view_mode=table"


    def __get_soup(self):
        page = requests.get(self.__url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "lxml")
            return soup
        else:
            self.__error_code = page.status_code
            return None
    
    
    def set_group(self, group: str):
        try:
            int(group)
        except ValueError:
            raise
        else:
            self.__group = group

    
    def parse_schedule(self):
        def __start_parser():
            self.__set_page_group()
            self.__soup = self.__get_soup()
        
        if self.__soup is None:
            return self.__error_code
        
        table = self.__soup.find("div", {"id": "table-container"})
        day_cards = table.find_all("div", {"class": "card"})

        def __process_card(day_card):
            def __get_day_name():
                return day_card.find("div", {"class": "card-header"}).find("h3").text
            
            def __get_day_data():
                def __get_tds(row):
                    return row.find_all("td")
                
                def __get_time(row):
                    all_time = row.find("th").text.split("-")
                    time_start = all_time[0]
                    time_end = all_time[1]

                    return time_start, time_end
                
                def __get_week(row):
                    return __get_tds(row)[0].find("i")['data-bs-title']

                def __get_classroom(row):
                    return __get_tds(row)[1].text

                def __get_group():
                    return int(self.__group)
                
                def __get_lesson(row):
                    info = __get_tds(row)[3]
                    return f"{info.find("span").text}\n{info.find("small").text}"

                
                def __get_teacher_img(row):
                    def __get_url():
                        img_tag = __get_tds(row)[4].find("img")
                        if img_tag is not None:
                            return img_tag["src"]
                        return None
                    
                    url = __get_url()
                    teacher_name = __get_teacher_name(row)
                    if url is not None:
                        img = requests.get(url)
                        return write_img_to_file(img, teacher_name)
                    return "no image"
                
                def __get_teacher_name(row):
                    name_in_a = __get_tds(row)[4].find("a")
                    if name_in_a is not None:
                        return validated_teacher_name(name_in_a.text)

                    name_in_span = __get_tds(row)[4].find("span")
                    if name_in_span is not None:
                        return validated_teacher_name(name_in_span.text)
                    
                    return "no name"

                table_body = day_card.find("tbody")
                rows = table_body.find_all("tr")
                

                res = []
                for row in rows:
                    time_start, time_end = __get_time(row)
                    week = __get_week(row)
                    classroom = __get_classroom(row)
                    group = __get_group()
                    lesson = __get_lesson(row)
                    teacher_img = __get_teacher_img(row)
                    teacher_name = __get_teacher_name(row)

                    res.append([time_start, time_end, week, classroom, group, lesson, teacher_img, teacher_name])
                return res
            

            day_name = __get_day_name()
            day_data = __get_day_data()

            return day_name, day_data
            
        res = {}
        for day_card in day_cards:
            day_name, day_data = __process_card(day_card)
            res[day_name] = day_data
        
        return res