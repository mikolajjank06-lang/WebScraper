# WebScraper

## Project implementation steps

### Stages 1-3

1. Provide URL of the product's opinion page
2. Send request to provided URL
3. Fetch product name
4. Fetch all opinions from the webpage
5. Parse opinions to extract required data
6. Check if there is a next page with opinions 
7. Repeat steps 4-6 for all pages with opinions about product
8. Save acquired opinions

## Project inputs
### Product codes

-133893145
-115761359
-115989910
-156627699
### Opinion structure
|component|name|selector|
|--------|----|--------|
|opinion ID|opinion_id|[data-entry-id]|
|opinion’s author|author|span.user-post_author-name|
|author’s recommendation|recomandation|span.user-post_authot-recomendation > em|
|score expressed in number of stars|score|span.user-post_score-count|
|opinion’s content|content|div.user-post_text|
|list of product advantages|pros|div.review-feature_item--positive|
|list of product disadvantages|cons|div.review-feature_item--negative|
|how many users think that opinion was helpful|helpful|button.vote-yes > span|
|how many users think that opinion was unhelpful|unhelpful|button.vote-no > span|
|publishing date|publish_date|span.user-post_published > time:nth-child(1)[]|
|purchase date|purchase_date|span.user-post_published > time:nth-child(2)[]|

