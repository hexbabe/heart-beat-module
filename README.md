# Heart Beat Generic Module

This module implements the [rdk generic API](https://github.com/rdk/generic-api) in the `seanorg:generic:heart-beat` model.

This module is very basic. It requires no config attributes and simply starts a background thread that +=1 a counter every second. The do_command returns the current value of the count as a dict {"count": <int>}

It was made to illustrate a possible Viam Python SDK logging bug where none of the logs in the background heart beat thread are ever handled and actually logged.
