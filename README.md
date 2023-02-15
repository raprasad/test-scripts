# test-scripts

This repository has two example Python scripts:

- `read_repository.py` - Read GitHub Issues
- `write_spreadsheet.py` - Write selected GitHub issue data to a spreadsheet

## Long Instructions

The instructions assume Python 3.7+ and ability to install packages via pip.

1. Install the requirements. 
    - ```pip install -r requirements.txt```
    - This was tested on Python 3.9 but should work with earlier versions
2. Set your GitHub auth token
   - Within the `src` directory, copy the file `auth_token_template.py` to `auth_token.py`
   - Follow the instructions within `auth_token.py`
      - ^ Be sure NOT to share this file/check it into GitHub
      - (It is already within the `.gitignore` file for this repository)
3. Set your repository
   - Open `settings_gh_repo.py` and the change the values to the appropriate repository ower and name 
4. Read the issues using the GitHub API and write them into one or more JSON files. The issue JSON is written to files, 100 issues per file--unless there are fewer than 100 issues.
   - Open a Terminal. Run the following:
     - `cd test-scripts/src`
     - `python read_repository.py`
   - For the output, look in the directory: 
     - `test-scripts/src/test_data/github_json/`
   - The files should be in there. The file name includes the repo owner, name, and a timestamp. If there are multiple files, there is also a page number.
     - Example of all issues in one file: 
       - `issues_opendp_crm_2023-02-15_16-19-48_all.json`
     - Example of issues in three files--note the "page number" in the file name: `_001`, `_002`, etc.
       - `issues_opendp_crm_2023-02-15_16-23-18_001.json`
       - `issues_opendp_crm_2023-02-15_16-23-18_002.json`
       - `issues_opendp_crm_2023-02-15_16-23-18_003.json`
6. Write an Excel file (.xlsx) using the data input. 
   - Find the file prefix, __without the page numbers__. In the last example in step (5), the file prefix is:
      - `issues_opendp_crm_2023-02-15_16-23-18`
   - Run the XLSX script using the file prefix. Example:
      - `python write_spreadsheet.py issues_opendp_crm_2023-02-15_16-19-48`
   - All of the input .json files with this prefix will be read, formatted, and written to a single .xlsx file.
   - For the output, look in the directory: 
     - `test-scripts/src/test_data/output/`

## Shorter Instructions

```
cd test-scripts

# (1) Install requirements
pip install -r requirements.txt

# (2) Set GitHub Auth Token
cp auth_token_template.py auth_token.py
# Add your token to auth_token.py

# (3) Set your GitHub repo to read from
# Update settings_gh_repo.py

# (4) Read issues
cd src
python read_repository.py 
# JSON files will be output to: test-scripts/src/test_data/github_json/
# Example output file name: issues_opendp_crm_2023-02-15_16-23-18_001.json

# (5) Write Excel 
# Find the prefix to your JSON files in (4)
# Example: "issues_opendp_crm_2023-02-15_16-23-18"
# ^ For the "prefix", don't include the trailing "_all.json" or page numbers like "_001.json", "_002.json"
# --------------------
# Run the next script using the prefix:
python write_spreadsheet.py issues_opendp_crm_2023-02-15_16-19-48

# Output will be: test-scripts/src/test_data/output/issues_opendp_crm_2023-02-15_16-19-48.xlsx
```
