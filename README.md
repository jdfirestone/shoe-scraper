## Why I Scraped this

As an advertising major, I wanted to work with a commercial site, and my interest for shoes made stockx.com the perfect choice. I used this site in the past to buy shoes and had to constantly check back to see when prices would change. Now with the ability to scrape the prices off the site, I can automate an alert system to tell me when prices dip below a certain price.

## How I scraped this

First I had to learn how to use and implement Selinium in order to load more of the screen I wanted to scrape. This would allow me to scrape the 560 items I wanted to.  Since stockx is a commercial site, normal scraping was blocked. I do this in get_page_contents.

Next, in get_urls, I scraped the urls from the page I loaded with Selinium and then put them into a list. Then list items are moved into a new list in order to add the first part of the link to each url. The full links are needed in order to grab all the details I need in the next step.

Finally, in get_shoe_info, the code loops through all the urls in the the previously made list and scrapes all the details from each pair of shoes. It also writes them line by line into a csv.

### Unexpected Problems

I ended up leaving the csv code outside of the function, because leaving it in the function would only let one row be written in the csv. That line would just be rewritten every time the loop ran.

I also tried to take the session and hdr variable out of the last function since they were defined globally. But after removing them I got errors that they were undefined for the req = session.get(url, headers=hdr) and bsObj = BeautifulSoup(req.text, "html5lib") lines. I ended up just leaving them in the function since it worked.

Ended up scraping 560 shoes, instead of 500. 

Thank you for your notes on my code this week! They were very helpful.
# shoe-scraper
# shoe-scraper
