chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.local.set({
    messengerDeletionInProgress: false,
    marketplaceChatsLoaded: false
  });

});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'deletionCompleted') {
    chrome.storage.local.set({
      messengerDeletionInProgress: false
    });
    chrome.runtime.sendMessage({
      action: 'deletionCompleted'
    });
    sendResponse({
      status: 'Deletion state updated to completed.'
    });
  } else if (request.action === 'deletionMarketplaceCompleted') {
    chrome.storage.local.set({
      marketplaceDeletionProgress: false
    });
    chrome.runtime.sendMessage({
      action: "deletionMarketplaceCompleted"
    });
    sendResponse({
      status: 'Deletion of marketplace updated to completed.'
    });
  } else if (request.action === 'loadingMarketplaceChats') {
    chrome.storage.local.set({
      marketplaceChatsLoaded: true
    });
    sendResponse({
      status: 'Marketplace Chats loaded.'
    });
  } else if (request.action === 'noMarketplaceFound') {
    chrome.storage.local.set({
      marketplaceChatsLoaded: false
    });
    sendResponse({
      status: 'No Marketplace Chats found.'
    });
  } else if (request.action === 'deletionMarketplaceProgressCompleted') {
    sendResponse({
      status: 'Marketplace deletion progress updated.'
    });
  }
});
