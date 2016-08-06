# DHeatmap
Simple script to sample commute time from [Google Directions API](https://developers.google.com/maps/documentation/directions/) from a given target address.
These samples are then interpolated to generate a dense heatmap that can be overlap to Google Maps. For an example see [commute time from ETH, Zurich](https://marcoancona.github.io/DHeatmap/)

## Usage

1. Generate your own [Google Directions API key](https://developers.google.com/maps/documentation/directions/).
2. Create a file simply named `key` in the main project folder with the only your key in it.
3. Set the coordinate of the region you want to sample from in `sample_distances.py`. 
**Set the maximum number of requests! Costs may apply if you sample more than the allowed free daily tier!**
4. Run `sample_distances.py` to start sampling. Results will be stored in `samples.txt`.
5. Run `draw_heatmap.py`to generate the heatmaps.


## Samples
By default this script samples random locations within a given area and provide commute time with public transport. Each location is sampled 3 times at different random times between 8AM and 8PM.
Two different figures are generated:

-`best`: the mean commute time assuming the departure is at the best time to avoid waiting for public means.

-`random`: the mean commute time assuming departure at random time.


## Integration in Google Maps
You can checkout the `gh-pages` branch of this repository to see a simple example of how the heatmap can be integrated in Google Maps.

## Result
You can see the result [here](https://marcoancona.github.io/DHeatmap/). The map shows commute time with public transport from the Swiss Federal Institute of Technology in Zurich.

## License
MIT
