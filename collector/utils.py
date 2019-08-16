from lxml import html as parse
import requests
import logging

logger = logging.getLogger(__name__)


def fill_target(target):
    # Fetch data for Target instance
    request = requests.get(target.url)
    tree = parse.fromstring(request.text)
    title = tree.xpath('//title')
    heading = tree.xpath('//h1')

    # Parse it
    target.encoding = request.encoding
    if title:
        target.title = title[0].text_content()
    if heading:
        target.heading = heading[0].text_content()

    # Task is completed
    target.to_handle = False
    # Instance is filled with data
    target.save()
