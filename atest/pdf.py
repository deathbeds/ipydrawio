""" do out-of-band things with the export server
"""
import requests


def get_ipydrawio_export_status(url):
    """get the ipydrawio export status"""
    r = requests.get(url)
    return r.json()
