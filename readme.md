# Get TOR UA : Get the current TOR User-Agent directly from it's source repo

---

### Why?

It's unfortunate that the `User-Agent` header is even required for traffic not to arouse suspicion.

But this is just the world we live in...

I like tor's useragent. It's generic, basic, common, and non-descriptive. 

In a world where you need a useragent string, this dummy info sould do the trick.

Unfortunately if you do an online search for `tor useragent` all of the results will be outdated.

instead of checking manually with tor-browser, this script will build the UA string from the source

---

### Usage:

```
$ python get_tor_ua.py

```

```
Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0

```
