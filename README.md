# py42
Python3 lib to interact with 42 API

## Usage

```sh
cd your_project &&
git clone git@github.com:thdelmas/py42.git
```

In your code
```python3
#!/usr/bin/env python3

from py42 import IntraAPI

if __name__ == '__main__':
	scopes = "profile public projects elearning tig forum"
	intra = IntraAPI.intraAPI(client_id, client_secret, 46, scopes, rate_limit)
	# Do whatever you want
	intra.closeConnection()
```
