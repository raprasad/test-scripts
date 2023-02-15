"""
Make some GitHub labels
"""
import sys
from collections import namedtuple, OrderedDict
import json
import requests
from msg_util import msgt, msg
from label_info import \
    (ESTIMATE_LABELS,
     ASK2ME_COMPONENTS)
import shared_vals


RepositoryInfo = namedtuple('RepositoryInfo', ['owner', 'repos'])



def edit_issue(issue_num):
    """Edit issue content"""
    owner = 'privacytoolsproject'
    repo = 'yarrow'

    body = """
1. **OpenAPI Definition**
    - [ ] Write definition
    - [ ] Write comments/docs
2. **Rust Runtime**
    - [ ] Write runtime
	- [ ] Implement tests
    - [ ] Write comments/docs
3. **Rust Validator**
    - [ ] Write validator
	- [ ] Implement tests
    - [ ] Write comments/docs
4. **Python bindings**
    - [ ] Create bindings
	- [ ] Implement tests
    - [ ] Write docs
5. **R bindings**
    - [ ] Create bindings
	- [ ] Implement tests
    - [ ] Write docs

    """
    edit_url = (f'{shared_vals.GH_API_URL}/repos/'
                f'{owner}/{repo}/issues/{issue_num}')

    params = dict(body=body,
                  labels=['PSI Core Library'],
                  #labels=['MVP', 'PSI Core Library'],
                  #milestone=1
                  )

    print('edit_url', edit_url)

    resp = requests.patch(edit_url, 
                          data=json.dumps(params),
                          headers=shared_vals.GH_HEADERS)
    msg(resp.status_code)

    if resp.status_code == 200:
        msg('label exists')
        return True

    if resp.status_code == 404:
        msg('Nope!')
        return False

    msg(resp.text)
    return False

if __name__ == '__main__':
    mvp_issues = [6, 7, 8, 9, 10, 14, 18, 20, 21, 22]
    print('mvp_issues', mvp_issues)
    #for issue in mvp_issues:
    #    edit_issue(issue)

    other_issues = [x for x in range(6, 24) if not x in mvp_issues]
    print('other_issues', other_issues)
    for issue in other_issues:
        edit_issue(issue)




body = """
- [ ] 1. Create **OpenAPI Definition**
- [ ] Write comments/docs
- [ ] 2. Write **Rust Runtime**
- [ ] Implement tests
- [ ] Write comments/docs
- [ ] 3. Write **Rust Validator**
- [ ] Implement tests
- [ ] Write comments/docs
- [ ] 4. Create **Python bindings**
- [ ] Implement tests
- [ ] Write docs
- [ ] 5. Create **R bindings**
- [ ] Implement tests
- [ ] Write docs

"""
