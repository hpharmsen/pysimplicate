# todo: add filter for invoice status


def invoice(self, filter={}):
    url = '/invoices/invoice?sort=id'
    for field in ('from_date', 'until_date'):
        if field in filter.keys():
            operator = 'ge' if field == 'from_date' else 'le'
            url = self.add_url_param(url, 'date', filter[field], operator)
    result = self.call(url)
    return result


def invoice_per_year(self, year):
    return self.invoice({'from_date': f'{year}-01-01', 'until_date': f'{year}-12-31'})
