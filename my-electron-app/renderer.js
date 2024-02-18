const { ipcRenderer } = require('electron');
const { spawn } = require('child_process');

function sendMessage() {
    const query = document.getElementById('query').value.trim();
    if (query) {
        addToChatLog('User', query);
        // Here you would typically send the query to the ChatGPT API and get a response
        const simulatedResponse = `To log in to your Charles Schwab account and check your checking account, please follow these instructions: `;
        addToChatLog('ChatGPT', simulatedResponse);
    }
    document.getElementById('query').value = ''; // Clear the input area
    document.getElementById('query').focus(); // Focus back to input area for next message
}

function addToChatLog(sender, message) {
  const chatLog = document.getElementById('chatLog');
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  if (sender === 'User') {
      messageElement.classList.add('user');
      messageElement.innerHTML = message;
  } else {
      messageElement.classList.add('chatgpt');
      messageElement.innerHTML = message;
  }
  chatLog.appendChild(messageElement);
  chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
}

let currentSteps = [];
let currentStepIndex = 0;
let flag = 1;

document.getElementById('send').addEventListener('click', function() {
    // displayNextStep();
    sendMessageToChatGPT(document.getElementById('query').value);
});

document.getElementById('query').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Prevent form from submitting
        sendMessageToChatGPT(document.getElementById('query').value);
    }
});

document.getElementById('nextStep').addEventListener('click', function() {
    displayNextStep();
});

function sendMessageToChatGPT(query) {
    // Simulated API response for demonstration purposes
    let py = spawn('python', ['./hello.py', flag, query])
    py.stdout.on('data', data => console.log('data : ', data.toString()))
    py.on('close', ()=>{
      
    })
    // const simulatedAPIResponse = "Locate the Login Area: On your screen, in the upper right corner, you will see two fields side by side. The field on the left is for your 'Login ID' and the one on the right is for your 'Password'.\nStep 2: Do something else.\nStep 3: Finish up.";
    currentSteps = ["Locate the Login Area: On your screen, in the upper right corner, you will see two fields side by side. The field on the left is for your 'Login ID' and the one on the right is for your 'Password'.", "Enter Login ID: Click on the Login ID box, then type in your unique Login ID that was created when you set up your account.", "Enter Password: Then, move to the next field to the right labeled 'Password'. Click on it and type in your password. Make sure to type it correctly as passwords are case sensitive.", "Log In: After entering your Login ID and Password, click on the blue 'Log in' button just to the right of the password field."];

    if (currentSteps.length > 0) {
      sendMessage();
      displayNextStep();
    }
}

function displayNextStep() {
    addToChatLog('ChatGPT', currentSteps[currentStepIndex]);
    if (currentStepIndex < currentSteps.length - 1) {
      document.getElementById('query').style.width = '0px';
      document.getElementById('query').style.padding = '0px';
      document.getElementById('send').style.height = '0px';
      document.getElementById('send').style.padding = '0px';
      document.getElementById('enableMicrophone').style.display = 'none';
      document.getElementById('nextStep').style.cssText = 'display: block !important;';
      currentStepIndex++;
    } else {
      document.getElementById('query').style.width = '100%';
      document.getElementById('query').style.padding = '10px 20px';
      document.getElementById('send').style.height = 'auto';
      document.getElementById('send').style.padding = '10px';
      document.getElementById('enableMicrophone').style.display = 'block';
      document.getElementById('nextStep').style.cssText = 'display: hidden !important;';
      document.getElementById('query').value = '';
      document.getElementById('query').focus(); // Focus back to input area for next message
      currentStepIndex = 0;
      flag = 2;
    }
}

document.getElementById('takeScreenshot').addEventListener('click', () => {
  ipcRenderer.send('take-screenshot');
});