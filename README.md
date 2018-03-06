# corpwechat
corp wechat utils, api(s) of corp wechat

## Usage

```python

from corpwechat import corpWechat
configpath = '/path/to/only_you_can_read_and_write.json'
cw = corpWechat(configpath)
tk = cw.get_token()
cw.push_text_msg(agentid=0, content='what you want to push'...)

