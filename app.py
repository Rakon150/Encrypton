from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ScndEncryption = 67
SpaceNum = 30
lowerCaseAlphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]

# Custom + Caesar encryption (merged)
def custom_encrypt(text, key):
    result = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            num = (ord(ch) - ord('A')) * key * ScndEncryption
        elif 'a' <= ch <= 'z':
            num = (ord(ch) - ord('a')) * key * ScndEncryption
        else:
            num = SpaceNum * key * ScndEncryption
        num += 9  # Caesar shift
        result.append(num)
    return ",".join(map(str, result))

def custom_decrypt(message, key):
    try:
        nums = [int(x) for x in message.split(",")]
    except ValueError:
        return "Invalid encrypted message format."
    decrypted = []
    for num in nums:
        num -= 9  # Reverse Caesar
        val = num // (key * ScndEncryption)
        if val == SpaceNum:
            decrypted.append(" ")
        else:
            decrypted.append(chr(val + ord('a')))
    return "".join(decrypted)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "POST":
        text = request.form["text"]
        key = int(request.form["key"])
        encrypted = custom_encrypt(text, key)
        return redirect(url_for("result", output=encrypted))
    return render_template("encrypt.html")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        message = request.form["message"]
        key = int(request.form["key"])
        decrypted = custom_decrypt(message, key)
        return redirect(url_for("result", output=decrypted))
    return render_template("decrypt.html")

@app.route("/result")
def result():
    output = request.args.get("output", "")
    return render_template("result.html", output=output)

if __name__ == "__main__":
    # Only open the browser when running in main thread and prevent double-tab
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    # Disable reloader to prevent multiple tabs
    app.run(debug=True, use_reloader=False)
