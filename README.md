# corpwechat
corp wechat utils, api(s) of corp wechat

## Usage

```python

from corpwechat import API
configpath = '/path/to/only_you_can_read_and_write.json'
api = API(configpath)
tk = api.get_token()
api.push_text_msg(agentid=0, content='what you want to push'...)

