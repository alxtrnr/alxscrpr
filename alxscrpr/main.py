import datetime
import gzip
import re
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import typer
from jinja2 import Template

pd.options.mode.chained_assignment = None  # default='warn'  # see https://stackoverflow.com/a/20627316/12576441
app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    A simple CLI URL scraper and xml site mapper.

    1. Reads an HTML document from a website, parses it and extracts all links to other pages/sites. Each link is printed
    out line by line to standard out. Prints only the URL, not any of the surrounding HTML tags or attributes. Prompts
    for an output directory to save a sitemap.

    2. Reads an HTML document saved to disk, parses it and extracts all links to other pages/sites. Each link is printed
    out line by line to standard out. Prints only the URL, not any of the surrounding HTML tags or attributes. Prompts
    for an output directory to save a sitemap.

    3. Takes in a URL file saved to disk containing all the sites to generate sitemaps for, prompts for an output
    directory to save sitemaps for each site in the inputs, and for the maximum number of URLs to include in a sitemap
    for extra-large sites.
    """
    if ctx.invoked_subcommand is None:
        options()


@app.command()
def options():
    """
    auto executes with no command
    """
    header = typer.style('Simple Scraper & Site Map Builder:', fg=typer.colors.BLACK, bg=typer.colors.YELLOW, bold=True)
    typer.echo()
    typer.echo(header)
    typer.echo()
    option1 = typer.style('1. Reads an HTML document from a website, parses it and extracts all links to '
                          'other pages/sites. Each link is printed out line by line to standard out.'
                          'Prints only the URL, not any of the surrounding HTML tags or attributes. Prompts for an '
                          'output directory to save a sitemap.', fg=typer.colors.WHITE)
    typer.echo(option1)
    option2 = typer.style('2. Reads an HTML document saved to disk, parses it and extracts all links to '
                          'other pages/sites. Each link is printed out line by line to standard out. '
                          'Prints only the URL, not any of the surrounding HTML tags or attributes. Prompts for an '
                          'output directory to save a sitemap.', fg=typer.colors.WHITE)
    typer.echo(option2)
    option3 = typer.style('3. Takes in a URL file saved to disk containing all the sites to generate'
                          'sitemaps for, prompts for an output directory to save sitemaps for each site '
                          'in the inputs, and for the maximum number of URLs to include in a sitemap for extra-large '
                          'sites.', fg=typer.colors.WHITE)
    typer.echo(option3)
    typer.echo()

    choice_text = typer.style('>>> url(1), local file(2), batch_sitemap(3)', fg=typer.colors.YELLOW, bold=True)
    choice = typer.prompt(choice_text)
    typer.echo(choice)

    if choice == '1':
        webpage()
    elif choice == '2':
        local_file()
    elif choice == '3':
        batch_process()


@app.command()
def local_file():
    """
    select from options
    """
    list_of_urls = []
    target = typer.style('Enter path to target file', fg=typer.colors.YELLOW, bold=True)
    target = typer.prompt(target)
    open_target = open(target)
    for line in open_target:
        if '&' in line:
            line.replace('&', '&amp;')  # https://www.sitemaps.org/protocol.html#escaping
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        # links = re.findall('"(http[s]?://.*?)"', line)
        for link in links:
            if link[-1] == ')':
                typer.echo(link[:-1])
                list_of_urls.append(link[:-1])

            else:
                typer.echo(link)
                list_of_urls.append(link)
    open_target.close()
    question = typer.style('Create sitemap (y/N)', fg=typer.colors.YELLOW, bold=True)
    question = typer.prompt(question)
    if question == 'y':
        site_map(list_of_urls)
    else:
        raise typer.Exit()


@app.command()
def webpage(target=None):
    """
    select from options
    """
    if not target:
        target = typer.style('Enter path to target webpage', fg=typer.colors.YELLOW, bold=True)
        target = typer.prompt(target)

    # connect to a URL
    req = Request(target, headers={'User-Agent': 'Mozilla/5.0'})

    # read html code
    web_byte = urlopen(req).read()
    web_page = web_byte.decode('utf-8')

    # use re.findall to get all the links
    links = re.findall('"(http[s]?://.*?)"', web_page)

    list_of_urls = []
    for link in links:
        if '&' in link:
            link.replace('&', '&amp;')  # https://www.sitemaps.org/protocol.html#escaping
        typer.echo(link)
        list_of_urls.append(link)

    question = typer.style('Create sitemap (y/N)', fg=typer.colors.YELLOW, bold=True)
    question = typer.prompt(question)
    if question == 'y':
        site_map(list_of_urls)
    else:
        raise typer.Exit()


@app.command()
def batch_process():
    """
    select from options
    """
    # open, read and parse file for urls
    list_of_urls = []
    file_to_process = typer.prompt('Enter path to file')
    opened_file = open(file_to_process)

    for line in opened_file:
        if '&' in line:
            line.replace('&', '&amp;')  # https://www.sitemaps.org/protocol.html#escaping
        links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        for url in links:
            if url[-1] == ')':
                typer.echo(url[:-1])
                list_of_urls.append(url[:-1])
            else:
                typer.echo(url)
                list_of_urls.append(url)
    opened_file.close()

    # send urls for site mapping
    for i in list_of_urls:
        webpage(i)


@app.command()
def site_map(list_of_links):
    """
    auto executes in run time
    """

    # save list to csv - see https://www.geeksforgeeks.org/python-save-list-to-csv/)
    rows = list_of_links
    np.savetxt("list_of_urls.csv", rows, delimiter=", ", fmt='% s')

    # sep, header and engine see: https://stackoverflow.com/a/26599892/12576441
    list_of_urls = pd.read_csv('list_of_urls.csv', sep='delimiter', header=None, engine='python')

    # Set-Up Maximum Number of URLs (recommended max 50,000)
    n = typer.style('set maximum number of URLs for extra-large sites', fg=typer.colors.YELLOW, bold=True)
    n = typer.prompt(n, default=1000)

    # Create New Empty Row to Store the Split File Number
    list_of_urls.loc[:, 'name'] = ''

    # Split the file with the maximum number of rows specified
    new_df = [list_of_urls[i:i + n] for i in range(0, list_of_urls.shape[0], n)]

    # For Each File Created, add a file number to a new column of the dataframe
    for i, v in enumerate(new_df):
        v.loc[:, 'name'] = str(v.iloc[0, 1]) + '_' + str(i)
        print(v)

    # Create a Sitemap Template to Populate  # https://www.sitemaps.org/protocol.html
    sitemap_template = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {% for page in pages %}
        <url>
            <loc>{{page[1]|safe}}</loc>
            <lastmod>{{page[3]}}</lastmod>
            <changefreq>{{page[4]}}</changefreq>
            <priority>{{page[5]}}</priority>        
        </url>
        {% endfor %}
    </urlset>'''

    template = Template(sitemap_template)

    # Get Today's Date to add as Lastmod
    lastmod_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Fill the Sitemap Template and Write File
    for i in new_df:  # For each URL in the list of URLs ...
        i.loc[:, 'lastmod'] = lastmod_date  # ... add Lastmod date
        i.loc[:, 'changefreq'] = 'daily'  # ... add changefreq
        i.loc[:, 'priority'] = '0.5'  # ... add priority

        # Render each row / column in the sitemap
        sitemap_output = template.render(pages=i.itertuples())

        # Create a filename for each sitemap like: sitemap_0.xml.gz, sitemap_1.xml.gz, etc.
        save_location = typer.style('path to save xml files', fg=typer.colors.YELLOW, bold=True)
        save_location = typer.prompt(save_location)
        filename = save_location + '_sitemap' + str(i.iloc[0, 1]) + '.xml.gz'

        # Write the File to Your Working Folder
        # For XML Validation error : EntityRef: expecting';' see https://stackoverflow.com/a/23422397/12576441")
        with gzip.open(filename, 'wt') as f:
            f.write(sitemap_output)
