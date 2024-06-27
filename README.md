# IndianKanoonScraper
This is a scraper for legal documents from [indiankanoon.org](https://indiankanoon.org/) built using BeautifulSoup and Selenium. It's configured to download the top x judgements of a court from each month of a specified year. 

## Customizations

The value of `URL` can be modified to change the court from which the judgements are retrieved (by default, documents are retrieved from National Green Tribunal Cases).

Setting `court_copy` to `True` when calling the download function will download court copies instead of the regular PDFs provided on the website. Make sure to enter your indiankanoon.org credentials in the appropriate fields, because court copies are only available for members.

The location of the downloads is set using `DOWNLOAD_DIR`. The default value is {current_dir}/green-tribunal-2022/. 

To run the script, call the download function, passing the `year` and value for `court_copy`.

## ChromeDriver

This scraper requires ChromeDriver to be installed on your system. Downloads and information here: [ChromeDriver Docs](https://developer.chrome.com/docs/chromedriver).

Set `CHROME_DRIVER_PATH` to the path to the ChromeDriver file you download.
