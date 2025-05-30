import sys
import os
import json
import logging
from modNixInput import nix_input

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "splunklib"))
from splunklib import modularinput as smi

class NixInputScript(smi.Script):

    def get_scheme(self):
        scheme = smi.Scheme("nix_input")
        scheme.description = "Read the 'ni' command source and ingest as JSON."
        scheme.use_external_validation = True
        scheme.use_single_instance = True
        scheme.streaming_mode = smi.Scheme.streaming_mode_simple
        return scheme

    def get_app_name(self):
        return "TA-hits-unix-ni"

    def validate_input(self, validation_definition):
        pass

    def stream_events(self, inputs, ew):
        instance_name = list(inputs.inputs.keys())[0]
        config = inputs.inputs[instance_name]
        instance_index = config.get("index") or "main"
        filename = config.get("file") or '/app/var/log/masterfile'
        instance_type = config.get("sourcetype") or "unix:hosts:json"
        ew.log(logging.INFO, f"Starting nix_input modular input: {instance_name}.")

        try:
            elements = nix_input(filename)
            for element in elements:
                # Create a Splunk event for each JSON element
                event = smi.Event(
                    data=json.dumps(element,separators=(',',':'))+"\n",
                    sourcetype=instance_type,
                    index=instance_index,
                    source=instance_name
                )
                event.stanza = instance_name
                ew.write_event(event)
            ew.log(logging.INFO, f"Finished nix_input modular input: {len(elements)}.")
        except json.JSONDecodeError:
            ew.log(logging.ERROR, "Failed to parse JSON.")
        except Exception as e:
            ew.log(logging.ERROR, f"Error: {e}")

if __name__ == "__main__":
    sys.exit(NixInputScript().run(sys.argv))
