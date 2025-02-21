# TA-hits-unix-ni

A Splunk technical add-on for feeding the UNIX team's server host inventory
to Splunk.

## Configuration

The only configuration that may need editing is the `inputs.conf`. The following are the attributes:

## Stanza: [nix_input://ni]

Multiple stanza may be created with the web UI. Below are descriptions of the attributes:

### sourcetype = unix:hosts:json

Defines the source type of this data input. Defaults to `unix:hosts:json`.

### source = <stanza>

Defines the source of this data. Defaults to the stanza name, e.g. `nix_input:ni`.

### interval = 14400

Interval for the instance to run. May be set to either number of seconds, or UNIX cron schedule.

### disabled = 0

Set to true to disable this input.

### index = main

Defines the index for this data to go to. Defaults to `main`.

### file = "/app/var/log/masterfile"

Defines the source file, defaults to `/app/var/log/masterfile`.

# Author
- Wei Wang <weiwang@med.umich.edu>
