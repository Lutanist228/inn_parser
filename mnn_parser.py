# АВТОР СКРИПТА: Александр Самохин. 
# СОАВТОРЫ СКРИПТА: нету

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time 
from math import ceil

URL = r"https://portal.eaeunion.org/sites/odata/redesign/Pages/InternationalNonProprietaryCodeClassifier.aspx"
s=Service(URL)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=s, options=options)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver.get(URL)
time_val = 10
sec = 1
res = 0 
position_fix = 0 
flag = False 
globe_dict = {} 
global_lst = [] 

def element_number_check(dig, i_1): # функция сверяет значение dig с настоящим id МНН-значения
    global driver
    global time_val
    global position_fix

    true_num_driver = WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="cell_{i_1}_0"]""")))
    time.sleep(sec)
    true_num = driver.find_element(By.XPATH, f"""//*[@id="cell_{i_1}_0"]""")
    time.sleep(sec)
    true_num = true_num.text
    true_num = list(true_num)
    num_list = [true_num.remove(true_num[0]) for i in range(len(true_num)) if true_num[0] == "0"]
    true_num = int("".join(true_num))

    if dig == true_num:
        position_fix = dig
        return dig # возвращает значение dig если оно совпадает с id. Type = integer.
    else:
        position_fix = true_num
        return true_num # возвращает значение true_num если значение dig не совпадает с id. Type = integer

def inner_auto(cell_list): # это по сути - основная функция которая слепливает все остальные функция друг с другом

    global dig
    global global_lst
    global percent
    global end_value
    global res 

    if flag == True:

        for i_1 in range(0, 30): 

            for num in range(1, 4):
                cell = f"cell_{i_1}_{num}"
                cell_list.append(cell)

            for i_2 in range(len(cell_list)): 
                elem_driver_find(cell_list[i_2], element_number_check(dig, i_1)) 

            cell_list.clear()  
            global_lst.clear() 

            if element_number_check(dig, i_1) == end_value:
                break 

            res += percent
            print(f"Loading data: {round(res, 2)}%")

            dig += 1
    else:
        for i_1 in range(0, 30): 

                for num in range(1, 4):
                    cell = f"cell_{i_1}_{num}"
                    cell_list.append(cell)

                for i_2 in range(len(cell_list)): 
                    elem_driver_find(cell_list[i_2], element_number_check(dig, i_1)) 

                cell_list.clear()  
                global_lst.clear() 

                res = percent * dig
                print(f"Loading data: {round(res, 2)}%")

                if element_number_check(dig, i_1) == end_value:
                    break 

                dig += 1

def to_current_page(num): # драйвер определяет на какой странице находится нужный нам (стартовый) элемент 
    # и переносит драйвер на нужную стрраницу

    c_page = WebDriverWait(driver, sec).until(EC.presence_of_element_located((By.XPATH, """//*[@id="eec-treeListView"]/div/div[2]/div/div/div/div/div[1]/div/div[1]/ul/li[3]/span/input""")))
    time.sleep(sec)
    c_page_drive = driver.find_element(By.XPATH, """//*[@id="eec-treeListView"]/div/div[2]/div/div/div/div/div[1]/div/div[1]/ul/li[3]/span/input""")
    c_page_drive.clear()
    time.sleep(sec)
    c_page_drive.send_keys(num)
    time.sleep(sec)
    c_page_drive.send_keys(Keys.RETURN)

def save_result(dict, file_name): # результат записывается в файл 
    with open(f"C:\\Users\\user\\Desktop\\IT-Project\\ProjectsPC\\File_test\\mnn_dict_res_{file_name}.txt", mode="w", buffering=-1, encoding="utf-8") as file:
        file.write(str(dict))
        print(f"Script has ended with the result: {dict}\n\n")
        print(f"File 'mnn_dict_res_{file_name}.txt' has been succesfully created.")
        k = input("Press any key to exit...")
    
def format_changer(): # парсер автоматически меняет формат для более удобного парсинга 

    global driver #принимается глобальное значение driver, полученное ранее
    global sec # время на сон между действиями ПО
    global time_val # время на поиск объекта

    time.sleep(sec)
    size_changer = WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="eec-page-size"]""")))
    size_find = driver.find_element(By.XPATH, """//*[@id="eec-page-size"]""")
    size_find.click()

    time.sleep(sec)

    format_changer = WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="eec-treeListView"]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div/div/ul/li[3]/a""")))
    format_find = driver.find_element(By.XPATH, """//*[@id="eec-treeListView"]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div/div/ul/li[3]/a""")
    format_find.click()
    time.sleep(sec)

def page_serfer(): # функция переключения на следующую страницу 

        page_searcher = WebDriverWait(driver,time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="eec-treeListView"]/div/div[2]/div/div/div/div/div[1]/div/div[1]/ul/li[4]/a""")))
        next_page = driver.find_element(By.XPATH, """//*[@id="eec-treeListView"]/div/div[2]/div/div/div/div/div[1]/div/div[1]/ul/li[4]/a""")
        next_page.click()
        time.sleep(sec)

def elem_driver_find(id_el, dig): # непосредственно поиск нужной информации и запись в виде словаря 
    global driver 
    global sec 
    global time_val 
    global globe_dict 
    global global_lst
    global file_num

    try:
        element = WebDriverWait(driver,time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="{id_el}"]"""))) 
        time.sleep(sec) 
        elem = driver.find_element(By.XPATH, f"""//*[@id="{id_el}"]""") 
        elem = elem.text 
        global_lst.append(elem)

        if len(global_lst) < 3: 
            globe_dict.update([(dig, global_lst.copy())])

        elif len(global_lst) == 3:
            globe_dict.update([(dig, global_lst.copy())])
            global_lst.clear()
    except TimeoutException:
        print()
        print(f"The element number {dig} wasn't found.\n")   
        print(f"Please, check whether an inputed information's correct.\n")

        print(f"The session has ended with: \n {globe_dict} \n\n")
        save_result(globe_dict, file_num)

def cell_auto(): # это как inner_auto. Она объединяет в себе другие функции 

    global global_lst # Подается список (global_lst = [])
    cell_list = []
    global min_element_position
    global max_element_position
    global end_value
    global dig
    global flag
    global res 


    if start_value == 1:

        inner_auto(cell_list)

    else:
        if flag == False:
            for i_1 in range(min_element_position, 30):

                for num in range(1, 4):
                    cell = f"cell_{i_1}_{num}"
                    cell_list.append(cell)

                for i_2 in range(len(cell_list)): 
                    elem_driver_find(cell_list[i_2], element_number_check(dig, i_1)) 

                cell_list.clear()  
                global_lst.clear() 
                flag = True

                if element_number_check(dig, i_1) == end_value:
                    break 

                res += percent
                print(f"Loading data: {round(res, 2)}%")

                dig += 1
        else:
            inner_auto(cell_list)

def driver_find(): # это - тело алгоритма. 

    global dig
    global globe_dict
    global current_page
    global final_page

    format_changer()

    if current_page > 1:
        to_current_page(current_page)

        for i in range(current_page, final_page + 1):

            cell_auto()

            if position_fix == end_value:
                print("Completed\n\n")
                return globe_dict

            page_serfer()

    else:
        for i in range(1, 313):

            cell_auto()

            if position_fix == end_value:
                print("Completed\n\n")
                return globe_dict

            page_serfer()

start_value = int(input("Введите, начиная с какого элемента парсить\n\n")) # для более удобной тестировки есть функционал задания 
# диапазона парсинга и удобное записывание в файл.
end_value = int(input("Введите до какого элемента парсить\n\n"))
min_element_position = (start_value % 30) - 1 
max_element_position = (end_value % 30) - 1 
current_page = ceil(start_value / 30)
print("The current page is", current_page, end="\n\n")
final_page = ceil(end_value / 30)
print("The final page is", final_page, end="\n\n")

if start_value == 1:
    percent = (100 * start_value) / end_value
else:
    total_elem = end_value - start_value
    percent = 100 / total_elem

dig = start_value

file_name = input("Print down the name of file to save the result\n\n")

print() 

save_result(driver_find(), file_name)

k = input()

