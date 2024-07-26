# Github Lines + Words Counter

A **Flask** Web application that allows you to enter a GitHub URL to count the number of Lines + Words in. 

Detects the most used language as well.

## TBI
- Language-wise word/line count
- Rank of most used languages in the project
- Currently shows the `extension` of the Programming language used. Need a dictionary to transpile each `ext` to `prog_lang_name` :(


## To Run:
`git clone https://github.com/suynep/github-lines-counter`

`cd github-lines-counter`

`python3 -m virtualenv .venv ;; init the virtualenv`

`. ./.venv/bin/activate ;; activate the venv`

`pip3 install -r requirements.txt`

`flask run`

## Screenshots

!(./assets-readme/ssproject1.png)
!(./assets-readme/ss2.png)