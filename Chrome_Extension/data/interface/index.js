function generateRandomString(length) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      result += characters.charAt(randomIndex);
  }
  return result;
}

function addMessageToChatBox(sender, message) {
  const chatBox = document.getElementById("chat-box");
  const messageElement = document.createElement("div");
  messageElement.classList.add(sender);
  messageElement.textContent = message;
  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}




var isCancelled = false;


var background = {
  "port": null,
  "message": {},
  "receive": function (id, callback) {
    if (id) {
      background.message[id] = callback;
    }
  },
  "connect": function (port) {
    chrome.runtime.onMessage.addListener(background.listener); 
    /*  */
    if (port) {
      background.port = port;
      background.port.onMessage.addListener(background.listener);
      background.port.onDisconnect.addListener(function () {
        background.port = null;
      });
    }
  },
  "post": function (id, data) {
    if (id) {
      if (background.port) {
        background.port.postMessage({
          "method": id,
          "data": data,
          "port": background.port.name,
          "path": "interface-to-background"
        });
      }
    }
  },
  "send": function (id, data) {
    if (id) {
      if (background.port) {
        if (background.port.name !== "webapp") {
          chrome.runtime.sendMessage({
            "method": id,
            "data": data,
            "path": "interface-to-background"
          }, function () {
            return chrome.runtime.lastError;
          });
        }
      }
    }
  },
  "listener": function (e) {
    if (e) {
      for (let id in background.message) {
        if (background.message[id]) {
          if ((typeof background.message[id]) === "function") {
            if (e.path === "background-to-interface") {
              if (e.method === id) {
                background.message[id](e.data);
              }
            }
          }
        }
      }
    }
  }
};

var config = {
  "current": {
    "style": '',
    "element": {
      "final": null,
      "interim": null
    }
  },
  "button": {
    "info": {},
    "talk": {},
    "final": {},
    "start": {},
    "dialect": {},
    "interim": {},
    "cancel": {},
    "language": {}
  },
  "linebreak": function (e) {
    return e.replace(/\n\n/g, "<p></p>").replace(/\n/g, "<br>");
  },
  "app": {
    "start": function () {
      config.speech.synthesis.init();
    }
  },
  "capitalize": function (e) {
    return e.replace(/\S/, function (m) {
      return m.toUpperCase();
    });
  },
  "show": {
    "info": function (i, q) {
      const comment = q ? '\n' + ">> " + q : '';
      config.button.info.textContent = ">> " + config.message[i] + comment;
    }
  },
  "nosupport": function (e) {
    config.button.start.disabled = true;
    config.button.dialect.disabled = true;
    config.button.language.disabled = true;
    config.button.talk.src = "images/nomic.png";
    config.show.info("no_support", e ? e : "Please either update your browser or try the app in a different browser.");
  },
  "selection": function () {
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
      /*  */
      const range = document.createRange();
      range.selectNode(config.button.final);
      window.getSelection().addRange(range);
    }
  },
  "fill": {
    "select": function () {
      config.button.language.textContent = '';
      for (let i = 0; i < config.language.length; i++) {
        config.button.language.add(new Option(config.language[i][0], i));
      }
      /*  */
      config.update.dialect(config.language[config.speech.synthesis.prefs.language]);
      config.button.language.selectedIndex = config.speech.synthesis.prefs.language;
      config.button.dialect.selectedIndex = config.speech.synthesis.prefs.dialect;
    }
  },
  "message": {
    "end": "Speech recognition is ended.",
    "no_speech": "No speech was detected!",
    "no_microphone": "No microphone was found!",
    "speak": "Please speak into your microphone...",
    "denied": "Permission to use the microphone was denied!",
    "blocked": "Permission to use the microphone is blocked!",
    "copy": "Press (Ctrl + C) to copy text (Command + C on Mac)",
    "start": "Speech to Text (Voice Recognition) app is ready.",
    "no_support": "Speech recognition API is NOT supported in your browser!",
    "allow": "Please click the - Allow - button to enable microphone in your browser."
  },

  
  // Function which records the value
  "start": function (e) {

    if (config.speech.synthesis.recognizing) {
      config.recognition.stop();
      config.show.info("copy");
      return;
    }

    isCancelled = false;
    config.speech.synthesis.start.timestamp = e.timeStamp;
    config.recognition.lang = config.button.dialect.value;
    config.speech.synthesis.final.transcript = '';
    config.speech.synthesis.ignore.onend = false;
    config.button.talk.src = "images/nomic.png";
    config.button.interim.textContent = '';
    config.button.final.textContent = '';

    config.button.cancel.disabled = false;

    config.recognition.start();
  },

  "cancel": function () {
  if (config.speech.synthesis.recognizing) {
    isCancelled = true; // Set the cancellation flag
    config.recognition.stop(); // Stop recognition when cancel is clicked
    config.show.info("canceled", "Speech recognition canceled.");

    // Clear any interim or final results
    config.button.interim.textContent = '';
    config.button.final.textContent = '';

    // Disable the cancel button after canceling
    config.button.cancel.disabled = true;

    // Reset the microphone button icon to the default state
    config.button.talk.src = "images/mic.png";
  }
},

  

  "callGoogleTTS": async function (text) {
    const apiKey = 'AIzaSyBxYQqW_QcvJD4NpmmGvJzubwKL-b6jMyw';
    const url = `https://texttospeech.googleapis.com/v1/text:synthesize?key=${apiKey}`;

    const requestData = {
      input: { text: text },
      voice: {
        languageCode: 'en-IN',
        name: 'en-IN-Standard-E', // Change to preferred voice
      },
      audioConfig: {
        audioEncoding: 'MP3',
        speakingRate: 1.0, // Adjust as needed
      },
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      const data = await response.json();

      // The API response contains audio content encoded in base64
      const audioContent = data.audioContent;

      // Convert the base64 string to an audio source and play it
      const audio = new Audio(`data:audio/mp3;base64,${audioContent}`);
      audio.play();
    } catch (error) {
      console.error('Error calling Google TTS:', error);
    }
  },

   "callApi": function (transcript) {
    console.log(transcript);

    let session_id = generateRandomString(5);

    // Display the user's message in the chat box
    addMessageToChatBox("user", transcript);

    // Storing user input
    const userKey = `user_${session_id}`;
    sessionStorage.setItem(userKey, transcript);
    
    fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: session_id,
        human_say: transcript
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Bot Response:', data);

      // Extract the bot's response text
      const botResponse = data.response;

      // Clean the bot's response text by removing backticks and other unwanted characters
      const cleanedBotResponse = botResponse.replace(/```/g, '');

      // Display the bot's message in the chat box
      addMessageToChatBox("bot", cleanedBotResponse);

      // Storing bot response
      const botKey = `bot_${session_id}`;
      sessionStorage.setItem(botKey, cleanedBotResponse);

      // Call Google TTS with the cleaned response
      config.callGoogleTTS(cleanedBotResponse);

      // Optional: Use browser's built-in TTS
      /*
      const utterance = new SpeechSynthesisUtterance(cleanedBotResponse);
      const voices = window.speechSynthesis.getVoices();
      const raviVoice = voices.find(voice => voice.name === 'Microsoft Ravi - English (India)');
      if (raviVoice) {
        utterance.voice = raviVoice;
      }
      utterance.pitch = 1.0;
      utterance.rate = 1.0;
      window.speechSynthesis.speak(utterance);
      */
    })
    .catch(error => {
      console.error('Error:', error);
    });
},

  "resize": {
    "timeout": null,
    "method": function () {
      if (config.port.name === "win") {
        if (config.resize.timeout) window.clearTimeout(config.resize.timeout);
        config.resize.timeout = window.setTimeout(async function () {
          const current = await chrome.windows.getCurrent();
          /*  */
          config.storage.write("interface.size", {
            "top": current.top,
            "left": current.left,
            "width": current.width,
            "height": current.height
          });
        }, 1000);
      }
    }
  },
  "flash": {
    "timeout": '',
    "element": document.querySelector(".start"),
    "stop": function () {
      config.flash.element.removeAttribute("color");
      if (config.flash.timeout) window.clearTimeout(config.flash.timeout);
    },
    "start": function () {
      if (config.flash.timeout) window.clearTimeout(config.flash.timeout);
      config.flash.element.setAttribute("color", "red");
      const _blink = function () {
        config.flash.timeout = window.setTimeout(function () {
          const color = config.flash.element.getAttribute("color") === "red" ? "white" : "red";
          config.button.start.setAttribute("color", color);
          _blink();
        }, 500);
      };
      /*  */
      _blink();
    }
  },
  "store": {
    "dialect": function () {
      config.speech.synthesis.prefs.dialect = config.button.dialect.selectedIndex;
      config.recognition.stop();
    },
    "language": function () {
      config.speech.synthesis.prefs.dialect = 0;
      config.speech.synthesis.prefs.language = config.button.language.selectedIndex;
      config.update.dialect(config.language[config.button.language.selectedIndex]);
      config.recognition.stop();
    }
  },
  "storage": {
    "local": {},
    "read": function (id) {
      return config.storage.local[id];
    },
    "load": function (callback) {
      chrome.storage.local.get(null, function (e) {
        config.storage.local = e;
        callback();
      });
    },
    "write": function (id, data) {
      if (id) {
        if (data !== '' && data !== null && data !== undefined) {
          let tmp = {};
          tmp[id] = data;
          config.storage.local[id] = data;
          chrome.storage.local.set(tmp);
        } else {
          delete config.storage.local[id];
          chrome.storage.local.remove(id);
        }
      }
    }
  },
  "port": {
    "name": '',
    "connect": function () {
      config.port.name = "webapp";
      const context = document.documentElement.getAttribute("context");
      /*  */
      if (chrome.runtime) {
        if (chrome.runtime.connect) {
          if (context !== config.port.name) {
            if (document.location.search === "?tab") config.port.name = "tab";
            if (document.location.search === "?win") config.port.name = "win";
            if (document.location.search === "?popup") config.port.name = "popup";
            /*  */
            if (config.port.name === "popup") {
              document.body.style.width = "650px";
              document.body.style.height = "550px";
            }
            /*  */
            background.connect(chrome.runtime.connect({"name": config.port.name}));
          }
        }
      }
      /*  */
      document.documentElement.setAttribute("context", config.port.name);
    }
  },
  "load": function () {
    const reload = document.getElementById("reload");
    /*  */
    config.button.talk = document.getElementById("talk");
    config.button.info = document.getElementById("info");
    config.button.start = document.getElementById("start");
    config.button.final = document.getElementById("final");
    config.button.interim = document.getElementById("interim");
    config.button.dialect = document.getElementById("dialect");
    config.button.language = document.getElementById("language");
    config.button.cancel = document.getElementById("cancel");
    config.current.element.final = document.querySelector(".container .results .final");
    config.current.element.interim = document.querySelector(".container .results .interim");
    /*  */
    config.button.start.addEventListener("click", config.start, false);
    config.button.dialect.addEventListener("change", config.store.dialect, false);
    config.button.language.addEventListener("change", config.store.language, false);
    config.button.cancel.addEventListener("click", config.cancel, false);
    /*  */
    reload.addEventListener("click", function () {
      document.location.reload();
    });
    /*  */
    config.storage.load(config.app.start);
    window.removeEventListener("load", config.load, false);
  },
  "update": {
    "dialect": function (target) {
      if (target) {
        config.button.dialect.textContent = '';
        config.button.dialect.style.visibility = "hidden";
        /*  */
        for (let i = 1; i < target.length; i++) {
          const value = target[i][0] !== undefined ? target[i][0] : '';
          const name = target[i][1] !== undefined ? target[i][1] : "System Default";
          const option = new Option(name, value);
          /*  */
          config.button.dialect.add(option);
          config.button.dialect.style.visibility = "visible";
        }
      }
    }
  },
  "speech": {
    "synthesis": {
      "recognizing": false,
      "ignore": {
        "onend": null
      },
      "final": {
        "transcript": ''
      },
      "start": {
        "timestamp": null
      },
      "init": function () {
        config.fill.select();
        config.show.info("start", "Please click on the microphone button to start speaking.");
        config.speech.synthesis.methods.oninit();
      },
      "prefs": {
        set dialect (val) {config.storage.write("dialect", val)},
        set language (val) {config.storage.write("language", val)},
        get dialect () {return config.storage.read("dialect") !== undefined ? config.storage.read("dialect") : 11},
        get language () {return config.storage.read("language") !== undefined ? config.storage.read("language") : 10},
      },
      "methods": {
        "onstart": function () {
          config.flash.start();
          config.speech.synthesis.recognizing = true;
          config.button.talk.src = "images/micactive.png";

          
          config.button.cancel.classList.add('enabled');
          /*  */
          const dialect = config.button.dialect[config.button.dialect.selectedIndex].textContent;
          const language = config.button.language[config.button.language.selectedIndex].textContent;
          /*  */
          config.show.info("speak", "Input language: " + language + ' > ' + dialect);
        },
        "onend": function () {
          config.speech.synthesis.recognizing = false;

          if (isCancelled) {
            return;
          }
          

          if (config.speech.synthesis.ignore.onend) return;
          /*  */
          config.flash.stop();
          config.button.talk.src = "images/mic.png";

          
          config.button.cancel.classList.remove('enabled');
          if (!config.speech.synthesis.final.transcript) {
            config.show.info("end", "No results to show! please try again later.");
            return;
          }

          config.callApi(config.speech.synthesis.final.transcript);
          /*  */
          config.selection();
          config.show.info("copy");
        },
        "onresult": function (e) {
          if (isCancelled) {
            return; // Do nothing if cancelled
          }

          const error = e.results === undefined || (typeof e.results) === "undefined";

          if (error) {
            config.recognition.onend = null;
            config.recognition.stop();
            config.nosupport();
            return;
          }
          /*  */
          let interim = '';
          for (let i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
              config.speech.synthesis.final.transcript += e.results[i][0].transcript;
            } else {
              interim += e.results[i][0].transcript;
            }
          }
          /*  */
          config.speech.synthesis.final.transcript = config.capitalize(config.speech.synthesis.final.transcript);
          config.button.final.textContent = config.linebreak(config.speech.synthesis.final.transcript);
          config.button.interim.textContent = config.linebreak(interim);
        },
        "onerror": function (e) {
          if (e.error === "no-speech") {
            config.flash.stop();
            config.button.talk.src = "images/mic.png";
            config.speech.synthesis.ignore.onend = true;
            config.show.info("no_speech", "Please click on the microphone button again.");
          }
          /*  */
          if (e.error === "audio-capture") {
            config.flash.stop();
            config.show.info("no_microphone");
            config.button.talk.src = "images/mic.png";
            config.speech.synthesis.ignore.onend = true;
          }
          /*  */
          if (e.error === "not-allowed") {
            const diff = e.timeStamp - config.speech.synthesis.start.timestamp;
            config.show.info(diff < 100 ? "blocked" : "denied");
            config.speech.synthesis.ignore.onend = true;
          }
        },
        "oninit": function () {
          window.SpeechRecognition = window.webkitSpeechRecognition || window.mozSpeechRecognition || window.SpeechRecognition;
          /*  */
          if (window.SpeechRecognition === undefined) {
            config.nosupport();
          } else {
            if (navigator.getUserMedia) {
              config.show.info("allow");
              navigator.getUserMedia({"audio": true}, function (stream) {
                if (stream.active) {
                  config.recognition = new window.SpeechRecognition();
                  /*  */
                  config.recognition.continuous = true;
                  config.recognition.interimResults = true;
                  config.recognition.onend = config.speech.synthesis.methods.onend;
                  config.recognition.onstart = config.speech.synthesis.methods.onstart;
                  config.recognition.onerror = config.speech.synthesis.methods.onerror;
                  config.recognition.onresult = config.speech.synthesis.methods.onresult;
                  config.show.info("start", "Please click on the microphone button to start speaking.");
                } else {
                  config.show.info("blocked", "Please reload the app and try again.");
                  config.speech.synthesis.ignore.onend = true;
                }
              }, function (e) {
                config.show.info("blocked", "Please reload the app and try again.");
                config.speech.synthesis.ignore.onend = true;
              });
            } else {
              config.nosupport();
            }
          }
        }
      }
    }
  }
};

document.addEventListener('DOMContentLoaded', (event) => {
  // Trigger the hello command on page load
  config.callApi("Hello, Flippi! How can you help me today?");
});

config.port.connect();

window.addEventListener("load", config.load, false);
window.addEventListener("resize", config.resize.method, false);