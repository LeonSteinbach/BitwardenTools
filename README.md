# BitwardenDuplicateRemover

## Description

This repository is a collection of tools for the usage of Bitwarden.
It contains:
* A tool for removing duplicate items in a json file exported with the Bitwarden Password Manager.
* A tool for merging a txt file exported from with the Kaspersky Password Manager into an existing json file exported with the Bitwarden Password Manager.

## Usage

Python 3 needs to be installed.

### Bitwarden duplicate remover
The tool expects two arguments:

```
python bitwarden_duplicate_remover.py input_file.json output_file.json
```

Arguments:
* input_file.json: The path to the exported json file
* output_file.json: The path to the json file that the tool should write the new json file without duplicates.

### Bitwarden Kaspersky merger

```
python bitwarden_kaspersky_merger.py input_bitwarden_file.json input_kaspersky_file.txt output_file.json
```

Arguments:
* input_bitwarden_file.json: The path to the json file exported by Bitwarden
* input_kaspersky_file.txt: The path to the txt file exported by Kaspersky
* output_file.json: The path to the json file that the tool should write the new merged json file.

## Important info

The input files are not overwritten and instead a new output file is generated. This is done to ensure the safety of not losing the original file in case the program fails.

### Bitwarden

**Tested with Bitwarden version 2024.4.1**

3 types of items are supported:
* Login ("type": 1)
* Card ("type": 2)
* Secure Note ("type": 3)

The json file format exported with Bitwarden is expected to look like this (**necessary fields only**). These are the fields that are used to create the hashes for detecting duplicates.

```
{
    ...,

    "items" : [
        ...,

        {
            ...,

            "type": 1,
            "name": "<name>",
            "notes": "<notes>",
            "login": {
                ...,

                "uris": [
                    {
                        "match": null,
                        "uri": "<uri>"
                    }
                ],
                "username": "<username>",
                "password": "<password>",
            }
        },

        ...,

        {
            ...,

            "type": 2,
            "name": "<name>",
            "notes": "<notes>",
        },

        ...,

        {
            ...,

            "type": 3,
            "name": "<name>",
            "notes": "<notes>",
            "card": {
                "cardholderName": "<cardholderName>",
                "brand": "<brand>",
                "number": "<number>",
                "expMonth": "<expMonth>",
                "expYear": "<expYear>",
                "code": "<code>"
            },
        },
    ]
}
```

### Kaspersky

**Tested with Kaspersky Password Manager version 24.0.0.428**

The txt file format exported with the Kaspersky Password Manager is expected to look like this.

```
Websites

Website name: <website_name_1>
Website URL: <website_url_1>
Login name: <login_name_1>
Login: <login_1>
Password: <password_1>
Comment: <comment_1>

---

Website name: <website_name_2>
Website URL: <website_url_2>
Login name: <login_name_2>
Login: <login_2>
Password: <password_2>
Comment: <comment_2>
<comment_2>

---

Applications

...

---

Notes

...

---

```

## Disclaimer

The following duplicate removal tool is provided as-is, without any warranties, expressed or implied. While efforts have been made to ensure its reliability, I do not guarantee the accuracy, completeness, or suitability of this tool for any particular purpose. Therefore, I cannot be held responsible for any direct or indirect damages, including but not limited to data loss, arising from the use or misuse of this tool.

It is recommended to thoroughly review and backup your data before utilizing this tool. By using this tool, you agree that you do so at your own risk and discretion.
