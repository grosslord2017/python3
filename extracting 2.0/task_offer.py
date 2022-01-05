import os
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from RPA.Excel.Files import Files
from time import sleep


site = Selenium()

url = "https://itdashboard.gov"
path = os.path.dirname(os.path.realpath(__file__)) + '/output/'
name_agency = 'Department of Labor'

site.open_available_browser(url=url, browser_selection='chrome')
site.set_download_directory(path)
site.click_element(site.get_webelement("css:a[aria-controls=home-dive-in]"))
site.wait_until_element_is_visible("css:div#agency-tiles-container")
element = site.find_element("css:div#agency-tiles-container")


def pull_off_values():
    agents = site.find_elements("css:a span.h4", element)
    agents_list = []
    for i in agents:
        agents_list.append(i.text)

    invests = site.find_elements("css:a span.h1", element)
    invests_list = []
    for i in invests:
        invests_list.append(i.text)

    btn = site.find_elements("css:a.btn", element)
    btn_list = []
    for i in btn:
        btn_list.append(i)

    # ------- если имя агенства которое нам надо, совпадает с именем в цикле перебора, то элемент кнопки этого
    # ------- агенства сохранить в переменную btn_elem
    result = []
    btn_elem = None
    for i in range(len(agents_list)):
        result.append([agents_list[i], invests_list[i]])
        if agents_list[i] == name_agency:
            btn_elem = btn_list[i]

    return result, btn_elem

def create_file():
    # create file
    FileSystem().create_directory(path)
    lib = Files().create_workbook()
    lib.save(f"{path}Агенства.xlsx")

def add_agencys_table(agency_list):
    agency_l = agency_list

    create_file()

    # open file and rename first sheet
    excel_file = Files()
    excel_file.open_workbook(f"{path}Агенства.xlsx")
    sheets = excel_file.list_worksheets()
    excel_file.rename_worksheet(sheets[0], 'агенства')

    # write in file
    for i in range(len(agency_l)):
        excel_file.set_cell_value(row=(i + 1), column=1, value=agency_l[i][0])
        excel_file.set_cell_value(row=(i + 1), column=2, value=agency_l[i][1])
    excel_file.save_workbook()

def add_table_af_agency():
    # open file
    excel_file = Files()
    excel_file.open_workbook(f"{path}Агенства.xlsx")
    sheets = excel_file.list_worksheets()
    if 'индивидуальные инвестиции' not in sheets:
        excel_file.create_worksheet(name='индивидуальные инвестиции')
    else:
        excel_file.remove_worksheet('индивидуальные инвестиции')
        excel_file.create_worksheet(name='индивидуальные инвестиции')

    site.wait_until_element_is_enabled("css:div#investments-table-object_wrapper", timeout=10)

    # check all elements in table
    check_all_elements = site.find_elements("css: label select.form-control option")
    for el in check_all_elements:
        if el.text == 'All':
            site.click_element(el)
        else:
            continue

    # waiting for the entire table to load
    all_table = site.find_element("css:div#investments-table-object_info").text
    n = all_table.split()
    number_rows_str = f'{" ".join(n[0:3])} {n[5]} {" ".join(n[4:])}'
    site.wait_until_element_contains("css:div#investments-table-object_info", text=number_rows_str, timeout=15)

    # filling the table
    main_table = site.find_element("css:table#investments-table-object")
    rows = site.find_elements("css:tbody tr", main_table)

    r_iter = 1
    for row in rows:

        download_pdf(row)

        columns = site.find_elements("css:td", row)
        col_iter = 1
        for cell in columns:
            excel_file.set_cell_value(row=r_iter, column=col_iter, value=cell.text)
            col_iter += 1
        r_iter += 1

    excel_file.save_workbook()

def download_pdf(row):
    try:
        el_ur = site.find_element("css:td.left.sorting_2 > a", row)
        pdf_url = str(site.get_element_attribute(el_ur, 'href'))
        site.open_available_browser(url=pdf_url, browser_selection='chrome')
        site.wait_until_element_is_enabled("css:div#business-case-pdf")
        pdf_file = site.find_element("css:div#business-case-pdf > a")
        start = load_check()
        while True:
            site.click_element(pdf_file)
            sleep(3)
            finish = load_check()
            if finish > start:
                break
            else:
                continue

        site.close_window()
    except:
        pass

def load_check():
    file_check = FileSystem()
    files = file_check.list_files_in_directory(path)
    return len(files)





agencys, btn_elem = pull_off_values()
add_agencys_table(agencys)
site.click_element(btn_elem)
add_table_af_agency()
