from bs4 import BeautifulSoup
import json
import copy

strhtml = BeautifulSoup(open('./original_data/original_data.html', encoding='utf-8'), features='html.parser')
# generalList = strhtml.select('#list')[0]
resultData = {} # 总数据
element_b = strhtml.select('#list>b') # 获取一级标题
element_ul = strhtml.select('#list>ul') # 获取一级列表数据
for index,tagB in enumerate(element_b):
    level_secend_name = {}
    level_secend_ul = element_ul[index]
    # 打断点看吧，说来复杂
    for index, element in enumerate(level_secend_ul.contents):
        level_third_name = {}
        if index %2 == 0 and element != '\n':
            level_third_name = {}
            for index, element_li in enumerate(level_secend_ul.contents[index +1]):
                if element_li != '\n' and element_li != ' ':
                    str = element_li.text.split('\n')[0]
                    level_fourth_name = []
                    element_dl = element_li.dl
                    element_dt_list = element_dl.find_all('dt') # 获取具体序列
                    element_dd_list = element_dl.find_all('dd') # 获取具体序列项
                    
                    for index, element_dt in enumerate(element_dt_list):
                        specific_item = element_dt_list[index].text + ' ' +element_dd_list[index].text
                        level_fourth_name.append(specific_item)

                    level_third_name[str] = copy.copy(level_fourth_name)

            level_secend_name[element.split('\n')[1]] = copy.copy(level_third_name)
    
    resultData[tagB.text] = copy.copy(level_secend_name)
    
# js = json.dumps(resultData)
# file = open('result.json', 'w')
# file.write(js)
# file.close()

# 去重
finalResult = {} #去重数据
for first_level in resultData:
    first = resultData[first_level]
    finalResult[first_level] = {}
    for secend_level in first:
        secend = first[secend_level]
        item = []
        for third_level in secend:
            item.extend(secend[third_level])
            resultSet = list(set(item))
            resultSet.sort()
        finalResult[first_level][secend_level] = resultSet

js = json.dumps(finalResult)
# 存入 JSON 文件
file = open('./deduplication_data/deduplication_data.json', 'w')
file.write(js)
file.close()

# 存入 txt 文件
file = open('./deduplication_data/deduplication_data.txt', 'w')
file.write(js)
file.close()


                


