# Prr: Personal Records App ()
## _The simplity of words in your personal records

Prr is a command line interfaces for save yours personal records for Weigthlifting

## Features

- List of your all last records movements
- List History records for movement
- List percentages of a record for a movement
- Create, update, delete a record for a movement

Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.
As [John Gruber] writes on the [Markdown site][df1]

> This project initial reason is present a proyect for course in a platzi

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Installation

Prr requires [Python](https://www.python.org) v3+ and [virtualEnv](https://virtualenv.pypa.io/en/latest/) to run.

configuration and run ours virtual enviroment
```sh
cd PersonalRecord
virtualenv venv
source ./venv/bin/activate
```

For stop off the virtual enviroment.

```sh
deactivate
```
Install the app
```sh
pip install .
```
## Commands

After install you can access to the funcionalities use:
```sh
prr records
```

| Command | Description |
| ------ | ------ |
| lists | Return All your last record for movement |
| movements | Return all movement avaliable for create records |
| Create {movement_id}| Add New record for a movement |
| update {movement_id} | Update a record for a movement |
| delete {movement_id} | Delete a record for a movement |
| get {movement_id} | Return list a porcentages for your last record for a movement |
| get {movement_id} -h | Return list history records for a movements |

## Work in progress.. 👉 👈

This is a first version for a app is my intension add adittional feature:
- Initial configuration for language and Weight unit.
- Export to CSV


## License

MIT

> The well-being of humanity, its peace and security are unattainable, unless its unity is firmly established.
> Bahá’u’lláh
**Free Software is a big step.******