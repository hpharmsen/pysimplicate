# Omzetgroepen
def revenuegroup(self):
    url = '/sales/revenuegroup'
    result = self.call(url)
    return result


def revenuegroup_dict(self):
    # Retrieves the list of revenue groups and caches it
    if not hasattr(self, '_revenuegroup_dict'):
        self._revenuegroup_dict = {r['label']: r['id'] for r in self.revenuegroup()}
    return self._revenuegroup_dict


def sales(self):
    url = '/sales/sales'
    result = self.call(url)
    return result


def sales_flat(self):
    return [
        {
            'organization': s['organization']['name'],
            'subject': s['subject'],
            'employee': double_get(s, 'responsible_employee', 'name'),
            'progress_label': s['progress']['label'],
            'progress_position': s['progress']['position'],
            'status': s['status']['label'],
            'start_date': s['start_date'],
            'modified': s['modified'],
            'source': double_get(s, 'source', 'name'),
            'expected_revenue': s.get('expected_revenue', 0),
            'chance_to_score': s['chance_to_score'],
            'value': s.get('expected_revenue', 0) * s.get('chance_to_score', 0) / 100,
        }
        for s in self.sales()
        if s['status']['label'] == 'OpportunityStatus_open'
    ]


def double_get(obj, first, second):
    if obj.get(first):
        return obj[first].get(second, '')
    return ''
