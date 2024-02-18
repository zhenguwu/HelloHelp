const { ipcRenderer } = require('electron');

function sendMessage() {
    const query = document.getElementById('query').value.trim();
    if (query) {
        addToChatLog('User', query);
        // Here you would typically send the query to the ChatGPT API and get a response
        const simulatedResponse = `Simulated response for "${query}"`;
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
    const simulatedAPIResponse = "Step 1: Do something.\nStep 2: Do something else.\nStep 3: Finish up.";
    currentSteps = simulatedAPIResponse.split('\n');

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
    }
}

document.getElementById('takeScreenshot').addEventListener('click', () => {
  ipcRenderer.send('take-screenshot');
});