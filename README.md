# Netflix Content Analytics

A data analysis project exploring the Netflix Movies & TV Shows catalog using **pandas**, **numpy**, and **matplotlib**.

## Dataset
`data/netflix_titles.csv` — 7,787 titles (Movies & TV Shows) with fields like type, director, cast, country, date added, release year, rating, duration, and genre.

## What this project answers
1. What's the split between Movies and TV Shows on Netflix?
2. How has the volume of content added to Netflix grown year over year?
3. Which countries produce the most content? (Top 10)
4. Which genres are most common on the platform? (Top 10)
5. What's the distribution of content ratings (age certifications)?
6. How long is a typical Netflix movie, statistically? (mean, median, std dev)

## Approach
- **Data cleaning:** handled missing values in `director`, `cast`, and `country` (filled with "Unknown" rather than dropping rows); dropped the small number of rows missing `date_added`/`rating`; converted `date_added` to a proper datetime type.
- **Feature engineering:** extracted `year_added` from the date; split the mixed-format `duration` field ("90 min" vs "3 Seasons") into a numeric value and a unit; extracted a single primary country from the comma-separated `country` field; exploded the comma-separated `listed_in` genre field into one genre per row for accurate genre counts.
- **Analysis:** used pandas `.value_counts()` and `.groupby()` for categorical breakdowns, and numpy for the movie duration statistics (mean/median/std).
- **Visualization:** matplotlib bar charts, a line chart for the year-over-year trend, and a histogram for the duration distribution — all saved as PNGs in `/output`.

## How to run
```bash
pip install -r requirements.txt
python analysis.py
```

Console output will print each finding, and all 6 charts will be saved to the `output/` folder.

## Key Insights
- Movies make up ~69% of the catalog vs ~31% TV Shows.
- Content additions peaked in 2019 before dropping off in the 2020–2021 data window.
- The United States and India are the two largest content-producing countries.
- "International Movies" and "Dramas" are the most common genres.
- The average Netflix movie runs about 99 minutes.
