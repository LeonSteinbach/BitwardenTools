import json
import sys
import datetime
import uuid


def read_json_from_file(filename):
    try:
        f = open(filename, "r")
    except OSError:
        print(f"Could not read file {filename}.")
        sys.exit(1)

    json_data = None

    with f:
        try:
            json_data = json.loads(f.read())
        except Exception as e:
            print(f"Invalid JSON syntax: {e}")
            sys.exit(1)
    
    return json_data


def write_json_to_file(json_data, filename):
    try:
        f = open(filename, "w+")
    except OSError:
        print(f"Could not write file {filename}.")
        sys.exit(1)
    
    string_data = None

    try:
        string_data = json.dumps(json_data, indent=2)
    except Exception as e:
        print(f"Invalid JSON syntax: {e}")
        sys.exit(1)
    
    with f:
        try:
            f.write(string_data)
        except Exception as e:
            print(f"Could not write file {filename}.")
            sys.exit(1)


def read_txt_from_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except OSError:
        print(f"Could not read file {filename}.")
        sys.exit(1)


def convert_txt_to_json_items(txt_data):
    items = txt_data.strip().split("\n\n---\n\n")
    parsed_items = []

    for item in items:
        parsed_data = {}
        lines = item.strip().split("\n")
        current_comment = ""

        for line in lines:
            if line.startswith("Comment:") or current_comment:
                if current_comment:
                    current_comment += "\n" + line
                else:
                    current_comment = "".join(line.split(": ")[1:])
            elif line.startswith("Website name:"):
                parsed_data["website_name"] = "".join(line.split(": ")[1:])
            elif line.startswith("Website URL:"):
                parsed_data["website_url"] = "".join(line.split(": ")[1:])
            elif line.startswith("Login name:"):
                parsed_data["login_name"] = "".join(line.split(": ")[1:])
            elif line.startswith("Login:"):
                parsed_data["login"] = "".join(line.split(": ")[1:])
            elif line.startswith("Password:"):
                parsed_data["password"] = "".join(line.split(": ")[1:])                
        
        if parsed_data:
            parsed_data["comment"] = current_comment

        if parsed_data:
            parsed_items.append(parsed_data)
    
    ignored_items = []
    result_items = []
    
    now = datetime.datetime.now(datetime.timezone.utc)
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"
    id = str(uuid.uuid4())

    for item in parsed_items:
        if not all([key in item.keys() for key in ["website_name", "website_url", "login_name", "login", "password", "comment"]]):
            ignored_items.append(item)
            continue

        result_item = {
            "passwordHistory": None,
            "revisionDate": formatted_time,
            "creationDate": formatted_time,
            "deletedDate": None,
            "id": id,
            "organizationId": None,
            "folderId": None,
            "type": 1,
            "reprompt": 0,
            "name": item["website_name"],
            "notes": item["comment"],
            "favorite": False,
            "login": {
                "fido2Credentials": [],
                "uris": [
                {
                    "match": None,
                    "uri": item["website_url"]
                }
                ],
                "username": item["login"],
                "password": item["password"],
                "totp": None
            },
            "collectionIds": None
        }

        result_items.append(result_item)

    if len(ignored_items) > 0:
        print(f"\nFailed to convert {len(ignored_items)} items.\n\
This is either because the item type is 'application' or 'note'\n\
or an error occured while parsing the item.")
        for item in ignored_items:
            print("    " + str(item))
        print("\n")
    
    return result_items


def merge_json(json_data, items_json):
    merged_data = json.loads(json.dumps(json_data))
    merged_data["items"].extend(items_json)
    return merged_data


def main():
    if len(sys.argv) != 4:
        print(f"Invliad number of arguments: Expected 3 \
(input bitwarden json file, input kaspersky txt file, output bitwarden json file) but got {len(sys.argv) - 1}.")
        sys.exit(1)
    
    bitwarden_filename = sys.argv[1]
    kaspersky_filename = sys.argv[2]
    output_filename = sys.argv[3]

    print("Reading bitwarden file...")
    bitwarden_json_data = read_json_from_file(bitwarden_filename)

    print("Reading kaspersky file...")
    kaspersky_txt_data = read_txt_from_file(kaspersky_filename)

    print("Converting kaspersky txt data to bitwarden json format...")
    kaspersky_json_items_data = convert_txt_to_json_items(kaspersky_txt_data)

    print("Merging data...")
    output_json_data = merge_json(bitwarden_json_data, kaspersky_json_items_data)

    print("Writing output file...")
    write_json_to_file(output_json_data, output_filename)

    print("Finished successfully!")


if __name__ == "__main__":
    main()
