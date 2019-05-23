from lib.base import NSOneBaseAction
from importlib import import_module
import json


class NSOneAction(NSOneBaseAction):
    """ NSOne run action
    """

    def run(self, module=None, package=None, method=None, **kwargs):
        """ Run action
        """
        self.logger.debug('Action running with Module: %s, Package: %s, Method: %s' % (
            module, package, method))

        # ns1-python depends too much on strategic None values, so any parameters that
        # have a value of None need to be discarded.
        for k, v in kwargs.items():
            if v is None:
                kwargs.pop(k)

        # Because most of the logic we care about is in sub modules, we need to
        # dynamically load the module and the package (Class)
        imported_module = import_module('ns1.rest.' + module, package=package)
        # Static Example: from ns1.rest.records import Records

        # With the loaded module, we need instantiate the package and pass it
        # our config (that has our API Key)
        loaded_package = getattr(imported_module, package)(self.ns1base.config)
        # Static Example: loaded_package =
        # ns1.rest.records.Records(self.ns1base.config)

        # Run the method() that was defined in the param 'method' in the
        # action's meta file
        result = getattr(loaded_package, method)(**kwargs)
        # Static Example: result = loaded_package.create(**kwargs)

        # Because successful delete actions result in an empty result (result: {})
        # we should look for this and return something useful
        if any(result):
            return (True, result)
        else:
            return (True, json.loads('{"deleted":true}'))
