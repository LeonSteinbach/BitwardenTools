# BitwardenDuplicateRemover

## Description

A Script for removing duplicate items in a json file exported with the Bitwarden password manager.

## Usage

Python 3 needs to be installed.
The tool expects two arguments:

```
python main.py input_file.json output_file.json
```

Arguments:
* input_file.json: The path to the exported json file
* output_file.json: The path to the json file that the tool should write the new json file without duplicates.

The input file is not overwritten and instead a new output file is generated. This is done to ensure the safety of not losing the original file in case the program fails.

## Important info

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
                        "uri": "http://zuehlke-careers.com"
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

## Disclaimer

The following duplicate removal tool is provided as-is, without any warranties, expressed or implied. While efforts have been made to ensure its reliability, I do not guarantee the accuracy, completeness, or suitability of this tool for any particular purpose. Therefore, I cannot be held responsible for any direct or indirect damages, including but not limited to data loss, arising from the use or misuse of this tool.

It is recommended to thoroughly review and backup your data before utilizing this tool. By using this tool, you agree that you do so at your own risk and discretion.