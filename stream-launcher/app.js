chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.create({
    url: 'http://localhost:5000/youtube-dl?url=' + btoa(tab.url)
  });
});
