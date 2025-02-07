# The nix_input function is used to get the nix input in JSON list format.
def nix_input ():
    result = subprocess.run(["/common/bin/ni", "--tojson"], capture_output=True, text=True, check=True)
    json_output = result.stdout
    return json.loads(json_output) if json_output else []
