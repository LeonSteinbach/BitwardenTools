import sys
import json


def get_hash_of_item(item):
    typ = item.get("type", None)
    name = item.get("name", None)
    login = item.get("login", None)
    notes = item.get("notes", None)
    card = item.get("card", None)
    
    if login is not None:
        username = login.get("username", None)
        password = login.get("password", None)
        return str(typ) + "_" + str(name) + "_" + str(notes) + "_" + str(username) + "_" + str(password)
    
    if card is not None:
        cardholderName = card.get("cardholderName", None)
        brand = card.get("brand", None)
        number = card.get("number", None)
        expMonth = card.get("expMonth", None)
        expYear = card.get("expYear", None)
        code = card.get("code", None)
        return str(typ) + "_" + str(name) + "_" + str(notes) + "_" + str(cardholderName) + "_" +\
            str(brand) + "_" + str(number) + "_" + str(expMonth) + "_" + str(expYear) + "_" + str(code)
    
    return str(typ) + "_" + str(name) + "_" + str(notes)


def remove_duplicates(json_data):
    hashes = set()
    unique_items = []

    items = json_data.get("items", None)
    if items is None or len(items) == 0:
        print("No items found in json file.")
        sys.exit(1)

    num_duplicates = 0

    for item in items:
        hash = get_hash_of_item(item)
        if hash not in hashes:
            hashes.add(hash)
            unique_items.append(item)
        else:
            num_duplicates += 1
    
    print(f"Removed {num_duplicates} duplicates of {len(items)} total items. \
{len(unique_items)} unique items remaining.")
    
    json_data["items"] = unique_items
    return json_data


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


def main():
    if len(sys.argv) != 3:
        print(f"Invliad number of arguments: Expected 2 \
(input json file, output json file) but got {len(sys.argv) - 1}.")
        sys.exit(1)
    
    old_filename = sys.argv[1]
    new_filename = sys.argv[2]

    print("Reading file...")
    json_data = read_json_from_file(old_filename)

    print("Removing duplicates...")
    json_data = remove_duplicates(json_data)

    print("Writing output file...")
    write_json_to_file(json_data, new_filename)

    print("Finished successfully!")

if __name__ == "__main__":
    main()
