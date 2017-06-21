# PhantomJS Integration Pack

This integration pack provides various integrations with
[PhantomJS](http://phantomjs.org/).

## Requirements (for running)

To be able to use actions inside this pack you need to have NodeJS and ``phantomjs-prebuilt``
NPM package installed on the system where the actions are being executed.

NPM package can be installed using npm:

```bash
npm -g install phantomjs-prebuilt
```

Keep in mind that the package needs to be installed and available globally on the system (``-g``
flag), otherwise you need to configure ``executable_path`` setting inside the config to point
to the PhantomJS executable (e.g.
``/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs``).

## Configuration

* executable_path - Path to the PhathomJS executable. Only needs to be specified if PhantomJS
  is not available inside ``$PATH`` globally on the system (see Requirements section above).

## Actions

* ``capture_screenshot`` - Capture a screenshot of the provided URL and save it on disk.
