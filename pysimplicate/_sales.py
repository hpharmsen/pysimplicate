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
