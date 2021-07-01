# todo: add filter for invoice status


def invoice(self, filter={}):
    url = '/invoices/invoice?sort=id'
    fields = {
        'from_date': 'date',
        'until_date': 'date',
        'project_number': 'projects.project_number',
        'invoice_number': 'invoice_number',
    }
    return self.composed_call(url, fields, filter)


def invoice_per_year(self, year):
    return self.invoice({'from_date': f'{year}-01-01', 'until_date': f'{year}-12-31'})


def invoice_lines(self, filter={}):
    def flatten_json(y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    invoices = self.invoice(filter)
    result = []
    for inv in invoices:
        a = len( inv['invoice_lines'])
        for line in inv['invoice_lines']:

            line_json = flatten_json(line)
            inv_json = flatten_json(inv)
            pass
    return None

def invoice_lines_per_year(self, year):
    return self.invoice_lines({'from_date': f'{year}-01-01', 'until_date': f'{year}-12-31'})

