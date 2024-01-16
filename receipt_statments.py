import jinja2
import pdfkit
from datetime import date
import sys
from dotenv import load_dotenv
import os
import logging
from framework_utils import config

root_path = config.get_root_path()
logger = config.configure_logging("log_py.log", logger_name=__name__)
today_date = date.today().strftime("%d.%m.%Y")


class PdfStatement:
    def __init__(self, user="Ime i Prezime", date="", items=[{'item': "fdscdtfd"}]):
        dotenv_path = (root_path + ".env")
        load_dotenv(dotenv_path=dotenv_path)
        self.save_location = root_path + os.getenv("statement_save_location")
        self.user = user
        self.full_name = ""
        if date == "" or date is None:
            self.date = today_date
        else:
            self.date = date
        self.items = items
        self.context = {}
        self.price = ""
        self.budget = ""
        self.payment = ""
        self.pdv = bool
        self.full_save_name = ""
        self.options = {
            'dpi': 365,
            'page-size': 'A4',
            'margin-top': '0in',
            'margin-right': '0.5in',
            'margin-bottom': '0in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None,
        }

        template_loader = jinja2.FileSystemLoader(root_path + 'templates/')
        self.template_env = jinja2.Environment(loader=template_loader)

    def zaduzenje(self):
        self.full_name = self.user
        # self.items = [{'item': "fdscdtfd"}, {'item': "fdscdtfd"}, {'item': "fdscdtfd"}, ]
        self.context = {'full_name': self.full_name, 'date': self.date, 'items': self.items}
        html_template = 'izjava_zaduzenje.html'
        template = self.template_env.get_template(html_template)
        output_text = template.render(self.context)
        self.full_save_name = f"Izjava o zaduzenju {self.full_name} {self.date}.pdf"
        pdfkit.from_string(output_text, self.save_location + self.full_save_name, css=root_path + 'static/css/statements.css', options=self.options)
        return self.full_save_name

    def zaduzenje_remote(self):
        self.full_name = self.user
        # self.items = [{'item': "fdscdtfd"}, {'item': "fdscdtfd"}, {'item': "fdscdtfd"}, ]
        self.context = {'full_name': self.full_name, 'date': self.date, 'items': self.items}
        html_template = 'izjava_zaduzenje_remote.html'
        template = self.template_env.get_template(html_template)
        output_text = template.render(self.context)
        self.full_save_name = f"Izjava o zaduzenju {self.full_name} {self.date}.pdf"
        pdfkit.from_string(output_text, self.save_location + self.full_save_name, css=root_path + 'static/css/statements.css', options=self.options)
        return self.full_save_name

    def razduzenje(self):
        self.full_name = self.user
        # self.items = [{'item': "fdscdtfd"}, {'item': "fdscdtfd"}, {'item': "fdscdtfd"}, ]
        self.items = self.items
        self.context = {'full_name': self.full_name, 'date': self.date, 'items': self.items}
        html_template = 'izjava_razduzenje.html'
        template = self.template_env.get_template(html_template)
        output_text = template.render(self.context)
        self.full_save_name = f"Izjava o razduzenju {self.full_name} {self.date}.pdf"
        pdfkit.from_string(output_text, self.save_location + self.full_save_name, css=root_path+'static/css/statements.css', options=self.options)
        return self.full_save_name

    def wifi_credentials(self, username, password):
        html_template = "izjava_wifi.html"
        template = self.template_env.get_template(html_template)
        self.context = {'username': username, 'password': password, 'date': self.date}
        output_text = template.render(self.context)
        pdf_bytes = pdfkit.from_string(output_text, False, css=os.path.join(root_path, 'static/css/statements.css'),
                                       options=self.options)
        return pdf_bytes

    # TODO:
    def mobitel(self, user="Ime i Prezime", date=today_date, items="Zaduženja", budget="600", price="500", pdv=True):
        self.full_name = user
        self.date = date
        self.items = [{'item': "fdscdtfd"}, {'item': "fdscdtfd"}, {'item': "fdscdtfd"}, ]
        self.budget = budget
        self.price = price
        if self.budget > self.price:
            self.payment = "0"
        else:
            self.payment = (int(self.price) - int(self.budget))
        if pdv == True:
            self.pdv = "+ PDV"
        else:
            self.pdv = ""

        self.context = {'full_name': self.full_name, 'date': self.date, 'items': self.items, 'budget': self.budget, 'price': self.price, 'payment': self.payment, 'pdv': self.pdv}

        html_template = 'izjava_mobitel.html'

        template = self.template_env.get_template(html_template)
        output_text = template.render(self.context)
        """
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        output_pdf = 'pdf_generated.pdf'
        pdfkit.from_string(output_text, output_pdf, configuration=config, css=root_path+'static/css/statements.css')
        """

        pdfkit.from_string(output_text, self.save_location + "Izjava-o-zaduzenju mobitela"+self.full_name+self.date+".pdf", css=root_path+'static/css/statements.css', options=self.options)


class Create:
    def zaduzenje(self, user="Ime i Prezime", date=today_date, items=[{'item': "fdscdtfd"}]):
        logger.info(f"date is {date=}{type(date)}")
        statement = PdfStatement(user=user, date=date, items=items)
        statement.zaduzenje()
        return statement.full_save_name

    def zaduzenje_remote(self, user="Ime i Prezime", date=today_date, items=[{'item': "fdscdtfd"}]):
        logger.info(f"date is {date=}{type(date)}")
        statement = PdfStatement(user=user, date=date, items=items)
        statement.zaduzenje_remote()
        return statement.full_save_name

    def razduzenje(self, user="Ime i Prezime", date=today_date, items=[{'item': "fdscdtfd"}]):
        statement = PdfStatement(user=user, date=date, items=items)
        statement.razduzenje()
        return statement.full_save_name

    def wifi_credentials(self):
        statement = PdfStatement()
        pdf = statement.wifi_credentials(username="Pero Perić", password="Password")
        with open("test_files/test.pdf", "wb") as pdf_file:
            pdf_file.write(pdf)


def test():
    izjava = Create().zaduzenje(user="zdenko")
    print(izjava)


if __name__ == "__main__":
    # test()
    Create().wifi_credentials()
