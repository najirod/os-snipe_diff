import jinja2
import pdfkit
from datetime import date
import sys
from dotenv import load_dotenv
import os

if "venv" in sys.path[0]:
    root_path = (sys.path[1] + "/")
else:
    root_path = (sys.path[0] + "/")

today_date = date.today().strftime("%d.%m.%Y")
#items = [{'item': "fdscdtfd"},{'item': "fdscdtfd"},{'item': "fdscdtfd"},]


class PdfStatment:
    def __init__(self):
        dotenv_path = (root_path + ".env")
        load_dotenv(dotenv_path=dotenv_path)
        self.save_location = os.getenv("statment_save_location")
        self.full_name = ""
        self.date = ""
        self.items = []
        self.context = {}
        self.price = ""
        self.budget = ""
        self.payment = ""
        self.pdv = bool
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

    def zaduzenje(self, user="Ime i Prezime", date=today_date, items="Zaduženja"):
        self.full_name = user
        self.date = date
        self.items = [{'item': "fdscdtfd"}, {'item': "fdscdtfd"}, {'item': "fdscdtfd"}, ]

        self.context = {'full_name': self.full_name, 'date': self.date, 'items': self.items}

        html_template = 'izjava_zaduzenje.html'

        template = self.template_env.get_template(html_template)
        output_text = template.render(self.context)
        """
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        output_pdf = 'pdf_generated.pdf'
        pdfkit.from_string(output_text, output_pdf, configuration=config, css=root_path+'static/css/statments.css')
        """

        pdfkit.from_string(output_text, self.save_location + "Izjava o zaduženju "+self.full_name+" "+self.date+".pdf", css=root_path+'static/css/statments.css', options=self.options)

    def razduzenje(self, user="Ime i Prezime", date=today_date, items="Zaduženja"):
        self.full_name = user
        self.date = date
        self.items = [{'item': "fdscdtfd"}, {'item': "fdscdtfd"}, {'item': "fdscdtfd"}, ]

        self.context = {'full_name': self.full_name, 'date': self.date, 'items': self.items}

        html_template = 'izjava_razduzenje.html'

        template = self.template_env.get_template(html_template)
        output_text = template.render(self.context)
        """
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        output_pdf = 'pdf_generated.pdf'
        pdfkit.from_string(output_text, output_pdf, configuration=config, css=root_path+'static/css/statments.css')
        """

        pdfkit.from_string(output_text, self.save_location + "Izjava o razduženju "+self.full_name+" "+self.date+".pdf", css=root_path+'static/css/statments.css', options=self.options)


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
        pdfkit.from_string(output_text, output_pdf, configuration=config, css=root_path+'static/css/statments.css')
        """

        pdfkit.from_string(output_text, self.save_location + "Izjava o zaduženju mobitela "+self.full_name+" "+self.date+".pdf", css=root_path+'static/css/statments.css', options=self.options)



def test():
    izjava = PdfStatment().mobitel(pdv=True)
    #izjava.zaduzenje()
    #izjava.razduzenje()


if __name__ == "__main__":
    test()