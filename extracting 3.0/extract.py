import os
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from robot.libraries.String import String
from time import sleep


class Extracting(object):
    def __init__(self):
        self.site = Selenium()
        self.file = FileSystem()
        self.excel = Files()
        self.pdf = PDF()
        self.string = String()
        self.url = "https://itdashboard.gov"
        self.path = os.path.dirname(os.path.realpath(__file__)) + '/output/'
        self.name_agency = 'Department of Labor'

    def start_programm(self):
        # self.create_directory()
        element = self.pars_first_page()
        agencys, btn_elem = self.pull_off_values(element)
        self.add_agencys_table(agencys)
        self.site.click_element(btn_elem)
        print('Waiting for files download')
        self.add_table_af_agency()
        print('Start comparing, please wait')
        temp = self.pars_excel()
        self.pars_all_pdf(temp)

    def create_directory(self):
        if self.file.is_directory_not_empty(self.path):
            self.file.remove_directory(self.path, recursive=True)
        self.file.create_directory(self.path)

    def open_url(self):
        self.site.open_available_browser(url=self.url, browser_selection='chrome', headless=True)
        self.site.set_download_directory(self.path)
        return

    def pars_first_page(self):
        self.open_url()
        self.site.click_element(self.site.get_webelement("css:a[aria-controls=home-dive-in]"))
        self.site.wait_until_element_is_visible("css:div#agency-tiles-container")
        element = self.site.find_element("css:div#agency-tiles-container")
        return element

    def pull_off_values(self, element):
        agents = self.site.find_elements("css:a span.h4", element)
        agents_list = []
        for i in agents:
            agents_list.append(i.text)

        invests = self.site.find_elements("css:a span.h1", element)
        invests_list = []
        for i in invests:
            invests_list.append(i.text)

        btn = self.site.find_elements("css:a.btn", element)
        btn_list = []
        for i in btn:
            btn_list.append(i)

        # if the name of the agency that we need is the same as the name in the iteration cycle,
        # then the element of this agency button is saved in the btn_elem variable
        result = []
        btn_elem = None
        for i in range(len(agents_list)):
            result.append([agents_list[i], invests_list[i]])
            if agents_list[i] == self.name_agency:
                btn_elem = btn_list[i]

        return result, btn_elem

    def create_file(self):
        self.file.create_directory(self.path)
        lib = self.excel.create_workbook()
        lib.save(f"{self.path}Agencies.xlsx")

    def add_agencys_table(self, agency_list):
        agency_l = agency_list

        self.create_file()

        # open file and rename first sheet
        self.excel.open_workbook(f"{self.path}Agencies.xlsx")
        sheets = self.excel.list_worksheets()
        self.excel.rename_worksheet(sheets[0], 'agencies')

        # write in file
        for i in range(len(agency_l)):
            self.excel.set_cell_value(row=(i + 1), column=1, value=agency_l[i][0])
            self.excel.set_cell_value(row=(i + 1), column=2, value=agency_l[i][1])
        self.excel.save_workbook()

    def add_table_af_agency(self):
        # open file
        self.excel.open_workbook(f"{self.path}Agencies.xlsx")
        sheets = self.excel.list_worksheets()
        if 'Individual Investments' not in sheets:
            self.excel.create_worksheet(name='Individual Investments')
        else:
            self.excel.remove_worksheet('Individual Investments')
            self.excel.create_worksheet(name='Individual Investments')

        self.site.wait_until_element_is_enabled("css:div#investments-table-object_wrapper", timeout=10)

        # check all elements in table
        check_all_elements = self.site.find_elements("css: label select.form-control option")
        for el in check_all_elements:
            if el.text == 'All':
                self.site.click_element(el)
            else:
                continue

        # waiting for the entire table to load
        all_table = self.site.find_element("css:div#investments-table-object_info").text
        n = all_table.split()
        number_rows_str = f'{" ".join(n[0:3])} {n[5]} {" ".join(n[4:])}'
        self.site.wait_until_element_contains("css:div#investments-table-object_info", text=number_rows_str, timeout=15)

        # filling the table
        main_table = self.site.find_element("css:table#investments-table-object")
        rows = self.site.find_elements("css:tbody tr", main_table)

        r_iter = 1
        for row in rows:

            self.download_pdf(row)

            columns = self.site.find_elements("css:td", row)
            col_iter = 1
            for cell in columns:
                self.excel.set_cell_value(row=r_iter, column=col_iter, value=cell.text)
                col_iter += 1
            r_iter += 1

        self.excel.save_workbook()

    def download_pdf(self, row):
        try:
            el_ur = self.site.find_element("css:td.left.sorting_2 > a", row)
            pdf_url = str(self.site.get_element_attribute(el_ur, 'href'))
            self.site.open_available_browser(url=pdf_url, browser_selection='chrome', headless=True)
            self.site.wait_until_element_is_enabled("css:div#business-case-pdf")
            pdf_file = self.site.find_element("css:div#business-case-pdf > a")
            start = self.load_check()
            while True:
                self.site.click_element(pdf_file)
                sleep(10)
                finish = self.load_check()
                if finish > start:
                    break
                else:
                    continue

            self.site.close_window()
        except:
            pass

    def load_check(self):
        files = self.file.list_files_in_directory(self.path)
        return len(files)

    def pars_excel(self):
        self.excel.open_workbook(f"{self.path}Agencies.xlsx")
        sheets = self.excel.list_worksheets()
        self.excel.set_active_worksheet(sheets[1])

        files_in_directory = self.file.list_files_in_directory(path=self.path)
        temp = []
        for i in range(1, len(files_in_directory)):
            a = self.excel.get_cell_value(column=1, row=i)
            b = self.excel.get_cell_value(column=3, row=i)
            temp.append([a, b])
        return temp

    def myGenerator(self, temp):
        for i in temp:
            yield i

    def pars_all_pdf(self, temp):
        number_files = self.file.list_files_in_directory(path=self.path)
        my_gen = self.myGenerator(temp)
        for i in number_files:
            try:
                elem = next(my_gen)
                if f'{elem[0]}.pdf' in i:
                    text = self.pdf.get_text_from_pdf(source_path=str(i), pages=1)
                    text1 = text[1]
                    d = self.string.get_regexp_matches(text1, r'(\d\.\s)(.)+\:\s(.)+\d{3}-\d{9}')[0]
                    # print(f'UII: {elem[0]}, Investment Title: {elem[1]}')
                    if elem[0] in d and elem[1] in d:
                        print(f'UII: {elem[0]}, Investment Title: {elem[1]} - comparing result: True')
                    else:
                        print(f'UII: {elem[0]}, Investment Title: {elem[1]} - comparing result: False')
            except:
                pass


if __name__ == '__main__':
    ext = Extracting()
    ext.start_programm()
