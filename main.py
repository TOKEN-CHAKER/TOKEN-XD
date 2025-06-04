from flask import Flask, request, render_template_string, redirect
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                message = f"{mn} {message1}"
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                parameters = {'access_token': access_token, 'message': message}
                try:
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        print(f"[✔️ SENT] {message}")
                    else:
                        print(f"[❌ FAIL] {response.status_code} {response.text}")
                except Exception as e:
                    print(f"[⚠️ ERROR] {str(e)}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    message = ""
    stop_message = ""
    if request.method == 'POST':
        if 'txtFile' in request.files:
            token_option = request.form.get('tokenOption')
            if token_option == 'single':
                access_tokens = [request.form.get('singleToken')]
            else:
                token_file = request.files['tokenFile']
                access_tokens = token_file.read().decode(errors='ignore').strip().splitlines()

            thread_id = request.form.get('threadId')
            mn = request.form.get('kidx')
            time_interval = int(request.form.get('time'))
            txt_file = request.files['txtFile']
            messages = txt_file.read().decode(errors='ignore').splitlines()

            task_id = 'BROKENNADEEM' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            stop_events[task_id] = Event()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
            threads[task_id] = thread
            thread.start()

            message = f'''
            <div style="padding:20INVALID gin-top:20px; background:black; color:lime; border-radius:15px; box-shadow: 0 0 15px lime; font-size:16px;">
            ✅ <b> YOUR LODER START SUCCESSFUL 🎉</b><br><br>
            🔑 <b>YOUR LODER STOP KEY ⤵️</b><br><br>
            <span style="color:red; font-size:18px;">{task_id}</span><br><br>
           [-NADEEM-] USE IT TO STOP THE PROCESS 
            </div>
            '''
        elif 'taskId' in request.form:
            task_id = request.form.get('taskId')
            if task_id in stop_events:
                stop_events[task_id].set()
                stop_message = f'''
                <div style="padding:20px; margin-top:20px; background:darkred; color:white; border-radius:15px; font-size:16px;">
                ✅ <b>YOUR LODER STOP SUCCESSFUL</b><br><br>
                YOUR STOP KEY ⤵️ <b>{task_id}</b>
                </div>
                <script>setTimeout(() => window.location.href = "/", 10000);</script>
                '''
            else:
                stop_message = f'''
                <div style="padding:20px; margin-top:20px; background:gray; color:white; border-radius:15px; font-size:16px;">
                ❌ <b>INVALID YOUR STOP KEY</b><br><br>
                <b>{task_id}</b>
                </div>
                <script>setTimeout(() => window.location.href = "/", 10000);</script>
                '''

    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
  <title>☠️🎋 OWNER BROKEN NADEEM 🎋☠️</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    html, body {
      height: 100%;
      margin: 0;
      background: url('https://i.ibb.co/hJWX8LwJ/IMG-20250307-WA0027.jpg') no-repeat center center fixed;
      background-size: cover;
      color: white;
      font-size: 16px;
    }
    .container {
      max-width: 95%;
      margin: 20px auto;
      background: rgba(0, 0, 0, 0.95);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 20px red;
    }
    .form-control {
      font-size: 14px;
      padding: 6px;
      height: auto;
    }
    .btn {
      font-size: 14px;
      padding: 6px;
    }
    label {
      font-size: 15px;
      margin-top: 8px;
    }
    h1 {
      font-size: 28px;
      text-shadow: 1px 1px red;
    }
    .glow {
      color: lime;
      font-size: 18px;
      text-align: center;
      padding: 12px;
      margin: 20px 0;
      background: black;
      border-radius: 15px;
      box-shadow: 0 0 12px lime;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="text-center text-danger">✨ BROKEN NADEEM ✨</h1>

    <form method="post" enctype="multipart/form-data">
      <label>⇣ S E L E C T ⇣ T O K E N ⇣ O P T I O N ⇣</label>
      <select class="form-control mb-2" name="tokenOption" id="tokenOption" onchange="toggleToken()" required>
        <option value="single">Single Token</option>
        <option value="multiple">Multiple Tokens (File)</option>
      </select>

      <div id="singleTokenDiv">
        <label>⇣ E N T E R ⇣ S I N G L E ⇣ T O K E N ⇣</label>
        <input type="text" name="singleToken" class="form-control mb-2">
      </div>

      <div id="tokenFileDiv" style="display:none;">
        <label>⇣ U P L O A D ⇣ T O K E N ⇣ F I L E ⇣</label>
        <input type="file" name="tokenFile" class="form-control mb-2" accept=".txt">
      </div>

      <label>⇣ E N T E R ⇣ C O N V O ⇣ I D ⇣</label>
      <input type="text" name="threadId" class="form-control mb-2" required>

      <label>⇣ E N T E R ⇣ H A T E R ⇣ N A M E ⇣</label>
      <input type="text" name="kidx" class="form-control mb-2" required>

      <label>⇣ E N T E R ⇣ S P E E D ⇣ (SECONDS) ⇣</label>
      <input type="number" name="time" class="form-control mb-2" min="1" required>

      <label>⇣ U P L O A D ⇣ M E S S A G E ⇣ F I L E ⇣</label>
      <input type="file" name="txtFile" class="form-control mb-2" accept=".txt" required>

      <button type="submit" class="btn btn-success w-100 mb-3">🚀 ⇣ S T A R T ⇣ L O D E R ⇣ 🚀</button>

      {{ message|safe }}
    </form>

    <form method="post">
      <label>⇣ E N T E R ⇣ S T O P ⇣ KEY ⇣</label>
      <input type="text" name="taskId" class="form-control mb-2" required>
      <button type="submit" class="btn btn-danger w-100">🛑 ⇣ S T O P ⇣ L O D E R ⇣ 🛑</button>

      {{ stop_message|safe }}
    </form>

    <div class="glow">Created By BROKEN NADEEM </div>
  </div>

  <script>
    function toggleToken() {
      const option = document.getElementById('tokenOption').value;
      document.getElementById('singleTokenDiv').style.display = (option === 'single') ? 'block' : 'none';
      document.getElementById('tokenFileDiv').style.display = (option === 'multiple') ? 'block' : 'none';
    }
  </script>
</body>
</html>
''', message=message, stop_message=stop_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
