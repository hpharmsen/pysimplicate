from simplicate import Simplicate
from settings import subdomain, api_key, api_secret


def show_projects(sim):
    for project in sim.projects():
        print( project )

if __name__=='__main__':
    sim = Simplicate(subdomain, api_key, api_secret)
    show_projects(sim)
