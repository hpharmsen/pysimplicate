# todo: add filter for invoice status
from collections import defaultdict


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


def invoiced_per_service(self, filter={}):
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
    result = defaultdict(float)
    for inv in invoices:
        if not inv.get('invoice_number'):
            continue  # conceptfactuur
        for line in inv['invoice_lines']:
            line_json = flatten_json(line)
            service_id = line_json.get('service_id', line_json['default_service_id'])
            result[service_id] += float(line_json['price']) * float(line_json['amount'])
    return result


def invoice_lines_per_year(self, year):
    return self.invoiced_per_service({'from_date': f'{year}-01-01', 'until_date': f'{year}-12-31'})
