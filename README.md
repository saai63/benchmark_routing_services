# Benchmark Routing Service Providers

## Motivation
Ola [recently announced the launch of it's own mapping services](https://www.linkedin.com/feed/update/urn:li:activity:7215988881886699521?updateEntityUrn=urn%3Ali%3Afs_feedUpdate%3A%28V2%2Curn%3Ali%3Aactivity%3A7215988881886699521%29). I wanted to benchmark the performance of Ola's maps against other service providers and this is a humble attempt at that. 
The framework can be further extended to benchmark other services such as Search, MapDisplay tiles etc.,

## How to run
Create environment variables required for each service providers such as Ola, Mapbox, TomTom, HERE. The names of the environment variables are "OLA_API_KEY", "MB_API_KEY", "TT_API_KEY" and "HERE_API_KEY" respectively.
Run the script benchmark_services.sh and see the benchmarks on the console. Responses from each service provider are saved as JSON files in the run directory.

## Results
When tested on a route from Mumbai to Bangalore, I see the following results.
```
+------------------+-----------------+--------------------+
| Service Provider |     Service     | Time taken (in ms) |
+------------------+-----------------+--------------------+
|       Ola        | Calculate route |      600.4735      |
|      Mapbox      | Calculate route | 203.12287500000002 |
|      TomTom      | Calculate route |     602.67725      |
|       Here       | Calculate route | 412.3824999999999  |
+------------------+-----------------+--------------------+
```
## Disclaimer
* I have used mostly the default request parameters.
* I cannot be certain if the parameters passed to each of the services are equivalent. The responses for each services need to be checked thoroughly and request parameters should be fine tuned to have a better comparison. 
