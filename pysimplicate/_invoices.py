def invoices(self, from_date: str = '', until_date: str = '', year=''):
    from_date_str, until_date_str = date_param(**locals())
    url = '/invoices/invoice?sort=id'
    if from_date_str:
        url = self.add_url_param(url, 'date', from_date, 'ge')
    if until_date_str:
        url = self.add_url_param(url, 'date', until_date, 'le')
    result = self.call(url)
    return result


def date_param(**kwargs):
    year = kwargs.get('year')
    from_date_str = kwargs.get('from_date_str')
    until_date_str = kwargs.get('until_date_str')
    assert year == '' or (
        from_date_str == '' and until_date_str == ''
    ), "you cannot specifiy both year and one of from_date_str and until_date_str"
    if year:
        return f'{year}-01-01', f'{year}-12-31'
    else:
        return from_date_str, until_date_str
