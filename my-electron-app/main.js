const { app, BrowserWindow, screen } = require('electron');

function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    const win = new BrowserWindow({
        width: width * 0.31,
        height: height,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        x: width - Math.round(width * 0.31), // Subtract the window width from the screen width
        y: 0
    });

    win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
