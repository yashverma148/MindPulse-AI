document.addEventListener('DOMContentLoaded', () => {
  const backendUrlInput = document.getElementById('backendUrl');
  const apiTokenInput = document.getElementById('apiToken');
  const timeRangeSelect = document.getElementById('timeRange');
  const autoSyncToggle = document.getElementById('autoSync');
  const syncBtn = document.getElementById('syncBtn');
  const statusDiv = document.getElementById('status');
  const lastSyncP = document.getElementById('lastSync');

  // Load saved settings
  chrome.storage.local.get(['backendUrl', 'apiToken', 'timeRange', 'autoSync', 'lastSync'], (result) => {
    if (result.backendUrl) backendUrlInput.value = result.backendUrl;
    if (result.apiToken) apiTokenInput.value = result.apiToken;
    if (result.timeRange) timeRangeSelect.value = result.timeRange;
    if (result.autoSync) autoSyncToggle.checked = result.autoSync;
    if (result.lastSync) lastSyncP.textContent = `Last synced: ${new Date(result.lastSync).toLocaleString()}`;
  });

  // Save settings on change
  const saveSettings = () => {
    chrome.storage.local.set({
      backendUrl: backendUrlInput.value.trim(),
      apiToken: apiTokenInput.value.trim(),
      timeRange: timeRangeSelect.value,
      autoSync: autoSyncToggle.checked
    });
  };

  backendUrlInput.addEventListener('input', saveSettings);
  apiTokenInput.addEventListener('input', saveSettings);
  timeRangeSelect.addEventListener('change', saveSettings);
  
  autoSyncToggle.addEventListener('change', () => {
    saveSettings();
    if (autoSyncToggle.checked) {
      chrome.alarms.create('autoSyncAlarm', { periodInMinutes: 60 });
    } else {
      chrome.alarms.clear('autoSyncAlarm');
    }
  });

  const showStatus = (msg, type) => {
    statusDiv.textContent = msg;
    statusDiv.className = `status-msg ${type}`;
    setTimeout(() => {
      statusDiv.textContent = '';
      statusDiv.className = 'status-msg';
    }, 3000);
  };

  syncBtn.addEventListener('click', () => {
    const backendUrl = backendUrlInput.value.trim();
    const apiToken = apiTokenInput.value.trim();
    const timeRange = parseInt(timeRangeSelect.value);

    if (!backendUrl || !apiToken) {
      showStatus('Please enter Backend URL and API Token.', 'error');
      return;
    }

    syncBtn.disabled = true;
    syncBtn.textContent = 'Syncing...';
    showStatus('Syncing data...', 'info');

    chrome.runtime.sendMessage({ action: 'syncHistory', backendUrl, apiToken, timeRange }, (response) => {
      syncBtn.disabled = false;
      syncBtn.textContent = 'Sync Now';

      if (chrome.runtime.lastError) {
        showStatus('Error communicating with background script.', 'error');
        return;
      }

      if (response && response.success) {
        showStatus(`Success! Synced ${response.saved} items.`, 'success');
        const now = new Date().toISOString();
        chrome.storage.local.set({ lastSync: now });
        lastSyncP.textContent = `Last synced: ${new Date(now).toLocaleString()}`;
      } else {
        showStatus(`Error: ${response ? response.error : 'Unknown error'}`, 'error');
      }
    });
  });
});
