# A Bot for Facebook Messenger!

> This bot is a hobby project to play with the Facebook messenger API and SqlAlchemy!. 
> Inspired by the [pymessemer][pym] repo.

## Pre-requisites

* Python>3.5

## Deployment

### Development environment

1. Clone the app.
2. Make sure to edit and rename the [env-sample][env] file to _.env_. Follow this [quickstart][fbqs] to set up the facebook environment variables. I used a free managed Posgresql service at [elephantsql][elps] as my database. 

```sh
$ python python -m pip -r install requirements.txt
$ cd Python-Messenger-Bot
$ python app.py
```

[pym]: <https://github.com/davidchua/pymessenger>
[env]: <env-sample>
[fbqs]: <https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start>
[elps]: <https://www.elephantsql.com/>