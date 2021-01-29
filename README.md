**A simple CLI URL scraper and xml site mapper.**

    1. Reads an HTML document from a website, parses it and extracts all links to other pages/sites. Each link is printed
    out line by line to standard out. Prints only the URL, not any of the surrounding HTML tags or attributes. Prompts
    for an output directory to save a sitemap.

    2. Reads an HTML document saved to disk, parses it and extracts all links to other pages/sites. Each link is printed
    out line by line to standard out. Prints only the URL, not any of the surrounding HTML tags or attributes. Prompts
    for an output directory to save a sitemap.

    3. Takes in a URL file saved to disk containing all the sites to generate sitemaps for, prompts for an output
    directory to save sitemaps for each site in the inputs, and for the maximum number of URLs to include in a sitemap
    for extra-large sites.


**How to Install**

The most popular way to install a Python package or library is to use pip. That's not possible here as the package
is not published to PiPy. You can instead install the package with a .whl file. Python wheel file ```.whl``` 
file is a specially formatted zip archive as a Python built-package. It contains all the installation files and may be 
installed by simply unpacking the file.


1. Check if pip is already [installed](https://pip.pypa.io/en/stable/installing/). 
    If pip.exe is not recognized, install it.

2. Download the .whl file from this repo  - dist/alxscrpr-0.1.0-py3-none-any.whl
   You could download an unofficial windows binary for Python extension packages from [UCI website](https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype).

3. Install the .whl file 
   For example, if you have downloaded ```this_package.whl``` to the folder ```C:\Downloads\```. 
   Use pip install ```C:\Downloads\this_package.whl``` to install the whl package file.

4. Run the CLI from terminal / command line by typing ```alxscrpr start```

**Demo**

If using Linux you're in luck! Linux has a builtin terminal command called script. Save the `dist/script_log` and 
`dist/scriptfile` in this repo to a local directory/folder. Open that directory in your terminal and type: 
```bash
scriptreplay --timing=script_log scriptfile
```
Your terminal will the playback a session recorded with script to go through the functionality of this CLI. Watch to the
end or just close the terminal when you have had enough! 
