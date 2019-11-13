## MapThingy

MapThingy is a simple Python + Javascript application that shows you where IP addresses and hostnames (such as `8.8.4.4` or `virgosvs.com`) are located on a Google Maps page. We are using [freegeoip.net](https://freegeoip.net/) to find the geographic location of our targets.

The system was built using:
* Python (either 2.7 or 3+ should work)
* [Tornado](http://www.tornadoweb.org/) as a Web and WebSocket server
* [Bulma](https://bulma.io) for simple CSS
* [Zepto.js](http://zeptojs.com) as a smaller jQuery
* [Lodash](https://lodash.com/) as a small utility box


### Getting started

If you are on Linux or macOS, you should be able to bootstrap the environment by running the following commands:

```
$ ./bootstrap.sh
$ source .env/bin/activate
```

To start the server, run the following command:

```
$ python mapthingy/server.py
```

And point your browser to [http://localhost:8888](http://localhost:8888).

### Assignment

1. When the page loads, the map isn't centered in San Francisco, correct that
2. There's a classmethod `APIHandler.is_hostname` on the `server.py` file that needs to be implemented. There's a simple test for it on the `tests.py` file, you can run this test by using pytest: `$ pytest mapthingy/tests.py`
3. The markers are generated without a title. [Google Maps API](https://developers.google.com/maps/documentation/javascript/markers) specifies a `title` attribute that could be used for adding the domain or IP address the marker belongs to.
4. freegeoip.net has a hard limit on how many requests can be made to the backend in a given hour. Implement a simple in-memory cache so that results that already exist don't need to be fetched again. [This StackOverflow question](https://stackoverflow.com/questions/12240285/how-to-share-data-between-requests-in-tornado-web) has a pointer on how to keep state between requests.
5. There's a "Find All" button on the page that currently isn't implemented. Using the existing API, implement it by sending each value in the comma-separated list of values to the API.
6. Extend the API to perform the "Find All" function in single request. The results should be streamed from the backend as they become available.
7. If you implemented #5 in a synchronous manner (by requesting all of the values in a loop on the server side), take a look at [Tornado's asynchronous HTTP client](http://www.tornadoweb.org/en/stable/httpclient.html) and figure out if there's a way you could speed up the retrieval of values from freegeoip.net by making the requests asynchronously.

#### BONUS round:
8. The [Google Maps marker API](https://developers.google.com/maps/documentation/javascript/markers) provides an `icon` attribute that could be used to display an image on the marker. Can you get our service to display the favicon for each data point that is a hostname/domain name?