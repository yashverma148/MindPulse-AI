chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'autoSyncAlarm') {
    chrome.storage.local.get(['backendUrl', 'apiToken', 'timeRange', 'autoSync'], (result) => {
      if (result.autoSync && result.backendUrl && result.apiToken) {
        performSync(result.backendUrl, result.apiToken, result.timeRange || 24);
      }
    });
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'syncHistory') {
    performSync(request.backendUrl, request.apiToken, request.timeRange)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Indicates asynchronous response
  }
});

async function performSync(backendUrl, apiToken, timeRangeHours) {
  try {
    const microsecondsPerDay = 1000 * 60 * 60 * 24;
    const startTime = (new Date).getTime() - (timeRangeHours * 60 * 60 * 1000);

    const historyItems = await new Promise((resolve) => {
      chrome.history.search({
        text: '',
        startTime: startTime,
        maxResults: 5000
      }, resolve);
    });

    const events = [];
    
    for (const item of historyItems) {
      if (!item.url || item.url.startsWith('chrome://') || item.url.startsWith('edge://')) {
        continue;
      }

      try {
        const urlObj = new URL(item.url);
        // Only send the origin for privacy, ignore query params and exact paths unless necessary.
        // We'll send domain and full clean url (without queries) if possible.
        let cleanUrl = urlObj.origin + urlObj.pathname;
        let domain = urlObj.hostname;
        
        // Remove www.
        if (domain.startsWith('www.')) {
          domain = domain.substring(4);
        }

        events.push({
          domain: domain,
          url: cleanUrl,
          title: item.title || '',
          last_visit_time: new Date(item.lastVisitTime).toISOString(),
          visit_count: item.visitCount || 1,
          typed_count: item.typedCount || 0
        });
      } catch (e) {
        // Invalid URL
        continue;
      }
    }

    if (events.length === 0) {
      return { success: true, saved: 0, skipped: 0 };
    }

    const payload = {
      source: 'chrome_extension',
      range_hours: parseInt(timeRangeHours),
      events: events
    };

    // Make sure url doesn't have trailing slash
    let url = backendUrl.endsWith('/') ? backendUrl.slice(0, -1) : backendUrl;

    const response = await fetch(`${url}/api/browser-history/sync`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiToken}`
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Server returned ${response.status}: ${errText}`);
    }

    const data = await response.json();
    if (data.success) {
      const now = new Date().toISOString();
      await chrome.storage.local.set({ lastSync: now });
    }
    
    return data;

  } catch (error) {
    console.error('Sync error:', error);
    throw error;
  }
}
