# todo: add filter for invoice status


def invoice(self, filter={}):
    url = '/invoices/invoice?sort=id'
    fields = {'from_date': 'date',
              'until_date': 'date',
              'project_number': 'projects.project_number',
              'invoice_number':'invoice_number'}
    return self.composed_call(url, fields, filter)


def invoice_per_year(self, year):
    return self.invoice({'from_date': f'{year}-01-01', 'until_date': f'{year}-12-31'})
