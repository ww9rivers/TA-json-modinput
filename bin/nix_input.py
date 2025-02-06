import sys
import os
import json
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "splunklib"))
from splunklib import modularinput as smi

class NixInputScript(smi.Script):

    def get_scheme(self):
        scheme = smi.Scheme("Nix Input")
        scheme.description = "Runs the 'nix' command and ingests its JSON output."
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True
        return scheme

    def validate_input(self, validation_definition):
        pass

    def stream_events(self, inputs, ew):
        instance_name = list(inputs.inputs.keys())[0]

        try:
            result = subprocess.run(["/common/bin/ni", "--tojson"], capture_output=True, text=True, check=True)
            json_output = result.stdout

            elements = json.loads(json_output) if json_output else []

            for element in elements:
                # Create a Splunk event for each JSON element
                event = smi.Event(
                    data=json.dumps(element),
                    sourcetype="hits:unix:hosts",
                    source=instance_name
                )
                ew.write_event(event)

        except subprocess.CalledProcessError as e:
            ew.log(smi.logging.ERROR, f"Error executing nix: {e}")
        except json.JSONDecodeError:
            ew.log(smi.logging.ERROR, "Failed to parse JSON.")

if __name__ == "__main__":
    sys.exit(NixInputScript().run(sys.argv))