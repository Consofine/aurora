## Northern Lights Notifier
I wrote this so I'd get notifications when the northern lights are active. I initially used Twilio, but recently switched to SMTP so I don't have to pay (or deal with Twilio). You can run this repo locally— I do so on a single board computer in my apartment so I don't have to pay for server costs but have it always available. See [this post](https://michaelconsidine.com/blog/building-a-northern-lights-notifier-in-python) for more background/info on the code.

### Setup
There are a few prerequisites before running this:
1. Install [tesseract](https://github.com/tesseract-ocr/tesseract)
2. Install all Python libraries in requirements.txt
3. (Optional) SMTP server if using SMTP. I downloaded [protonmail-bridge](https://proton.me/mail/bridge) so I could do this locally. [This guide](https://medium.com/@vdugnist/how-to-send-emails-programmatically-with-protonmail-c1d760985957) was helpful. Otherwise, I'm sure this could easily be adapted to use Gmail or something (boooo Google having access to all your emails).
4. Set up env vars:
  - If using Twilio:
    - `TWILIO_AUTH_TOKEN`
    - `TWILIO_ACCOUNT_SID`
    - `TWILIO_FROM_NUMBER`
    - `TWILIO_TO_NUMBER`
  - If using SMTP:
    - `TO_EMAIL`
    - `FROM_EMAIL`
    - `FROM_EMAIL_PASSWORD` (**note**: for protonmail bridge, this is the password you get from your settings or by running `info` in the CLI after you've logged in. It is **not** your normal email password.)

### Running
Can just run this with `python main.py` (or `python3` or whatever). Other tips:
- To run in the background: `python main.py &`
- Or open a tmux session, run it there, and close without killing the session
