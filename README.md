# A notification server that sends notifications to Google Home

This is a webservice that has six endpoints:

- /play/ - plays an mp3 on the google home that is in the static folder
- /say - uses googles unofficial google translate TTS service to say a notification
- /youtube/play uses youtube to play songs
- /facebook/messenger/say use facebook messenger to send message
- /android/sms/send send a sms via ifttt
- /google/home/adapter adapt a simple argument api to a multiple arguments one 

# use

## getting started

This uses flask and you should just be able to install the requirements: `pip install -r requirements.txt` and then run the webservice `python app.py`

You will have to edit `app_config.py` and fill all the parameters.

## URLs

`/play/mp3name.mp3`

This will play mp3name.mp3 over the google homes. I put two mp3s in the static dir for you to try out: JR.mp3 and doorbell1.mp3. Try them: `/play/JR.mp3` or `/play/doorbell1.mp3`

`/say?text=Oh My God this is awesome`

Just pass a GET variable to the `/say` endpoint and the google homes will say your text. It also caches this so that the second time it will be a bit quicker than the first time. yay. 

You can also do other languages too: 

`/say/?text=猿も木から落ちる&lang=ja` 

`youtube/play?query=Oh My Sweet Lord`

This will play the first song returned by youtube matching the corresponding query

`/facebook/messenger/say`

This will send a message to one of your friend on facebook messenger. You need to provide two POST variables `to`
and `message` to use it.

`/google/home/adapter?token=messenger` and

`/google/home/adapter?token=Alice` and

`/google/home/adapter?token=Hello There!`

This will buffer method name and every single parameters and then will call the corresponding API

`/android/sms/send`

This will send a sms to someone. You need to provide two POST variables `to` and `message` to use it.
You must before using it create an endpoint on ifttt

## running for real

I use docker to run it. It works pretty well.

run with:
```bash
docker build -t google-home-apis:latest .
docker run --restart=always -d -p 8080:8080 google-home-apis
```

# How

Google homes are just chromecasts! Who knew! You just have to treat them like chromecasts. They show up when you browse for chromecasts via python or any other code library. You can then just send audio their way. 
