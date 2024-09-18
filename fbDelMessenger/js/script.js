/*
 **************************************************
 * WARNING: Unauthorized copying, distribution,    *
 * or use of this code, in whole or in part,       *
 * without explicit permission from the author,    *
 * is strictly prohibited. Legal action will be    *
 * taken against any individual or organization    *
 * found to be in violation of this notice.        *
 * This code is protected by copyright laws.       *
 **************************************************
 */

let isChatsDeletionStopped = false;
let isMarketplaceChatsDeletionStopped = false;
let isArchiveStopped = false;
let msgCount = 0;
let mrktCount = 0;
let archivCount = 0;
let mrktIntvl1;
let mrktIntvl2;
let msgIntvl1;
let msgIntvl2;
let archivInt1;
let archivInt2;


window.onload = function () {
  chrome.storage.sync.set({
    marketplaceChatsLoaded: false
  });
}

// Message listener from background script
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "startChatsDeletion") {
    isChatsDeletionStopped = false;
    msgCount = 0;
    startMessengerDeletion();
    console.log("Received startChatsDeletion message.");
    sendResponse({
      status: "Chats deletion started."
    });
  } else if (request.action === "stopChatsDeletion") {
    stopMessengerDeletion();
    console.log("Received stopChatsDeletion message.");
    sendResponse({
      status: "Chats deletion stopped."
    });
  } else if (request.action === "loadMarketplaceChats") {
    loadMarketplaceChats();
    console.log("Received loadMarketplaceChats message.");
    sendResponse({
      status: "Loading marketplace Chats on page."
    });
  } else if (request.action === "startMarketplaceDeletion") {
    isMarketplaceChatsDeletionStopped = false;
    mrktCount = 0;
    console.log("Received startMarketplaceDeletion message.");
    startMarketplaceDeletion();
    sendResponse({
      status: "Start Marketplace Chats Deletion."
    });
  } else if (request.action === "stopMarketplaceDeletion") {
    stopMarketplaceDeletion();
    console.log("Received stopMarketplaceDeletion message.");
    sendResponse({
      status: "Stop Marketplace Chats deletion."
    });
  } else if (request.action === 'startArchive') {
    archivCount = 0;
    isArchiveStopped = false;
    startArchive();
    sendResponse({
      status: 'Archive Messages Start'
    });

  } else if (request.action === 'stopArchive') {
    stopArchive();
    sendResponse({
      status: 'Archive Messages Stoppped'
    })
  }
});

document.addEventListener('click', function (event) {
  const clickedElement = event.target.closest('[aria-label] i[data-visualcompletion="css-img"]');
  if (clickedElement) {
    handleButtonClick();
  }
});

function handleButtonClick() {
  chrome.runtime.sendMessage({
    action: 'backButtonClicked'
  });
}

const selectors = {
  grid: {
    container: 'div[role="grid"]',
    cell: 'div[role="gridcell"]',
    row: 'div[role="row"]',
    button: 'div[role="button"]'
  },
  menu: {
    menu: 'div[role="menu"]',
    item: 'div[role="menuitem"]'
  },
  dialog: {
    confirmButton: 'div[role="dialog"] > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div[role="button"]'
  },
  svg: {
    menuDots: 'path[d*="M458 408a2 2 0 1 1-4"]',
    mrktPlc: 'path[d*="M109.291 919c.18"]',
    deleteChat: 'path[d*="m106.523 196.712-2.32-2.256a1.62 1.62 0 0 0-1.13-.456h-3.146"]',
    leaveGroup: 'path[d*="M105 220.75v2.855a.9.9 0 0"]'
  }
};



// Function to start the deletion process for messenger chats
function startMessengerDeletion() {
  const eachChat = $(`
    ${selectors.grid.container} 
    ${selectors.grid.cell} 
    ${selectors.grid.button}
    ${selectors.svg.menuDots}
    `);
  if (eachChat.length) {
    if (isChatsDeletionStopped) {
      return;
    }
    eachChat.first().closest(selectors.grid.button).click();
    msgIntvl1 = setInterval(function () {
      const eachChatMenu = $(`
        ${selectors.menu.menu}
        ${selectors.menu.item}
        ${selectors.svg.deleteChat}
        `);
      if (eachChatMenu.length) {
        eachChatMenu[0].closest(selectors.menu.item).click();
        clearInterval(msgIntvl1);
        msgIntvl2 = setInterval(function () {
          const confirmDeleteMsgChatButton = $(selectors.dialog.confirmButton);
          if (confirmDeleteMsgChatButton.length) {
            confirmDeleteMsgChatButton[0].click();
            clearInterval(msgIntvl2);
            msgCount++;
            showingMessnegerMsg();
            setTimeout(() => {
              startMessengerDeletion();
            }, 1000);
          }
        }, 500);
      }

    }, 500);


  } else {
    isChatsDeletionStopped = false;
    console.log("All Deleted / No chats found!");
    Swal.fire({
      title: 'Messenger Chat',
      text: 'All Deleted / There are no Messenger Chats.',
      icon: 'info'
    });
    chrome.runtime.sendMessage({
      action: 'deletionCompleted'
    });
  }
}

function showingMessnegerMsg() {
  chrome.runtime.sendMessage({
    action: "trialsLimit",
    count: msgCount
  });
  chrome.runtime.sendMessage({
    action: 'deletionProgress',
    progress: msgCount
  });
}

// Function to stop the deletion process for messenger chats
function stopMessengerDeletion() {
  isChatsDeletionStopped = true;
  clearInterval(msgIntvl1);
  clearInterval(msgIntvl2);
  chrome.runtime.sendMessage({
    action: 'deletionCompleted'
  });
  Swal.fire({
    title: 'Stopped',
    text: 'You can restart deletion after page reload.',
    icon: 'warning',
    confirmButtonText: 'OK',
    allowOutsideClick: false,
    allowEscapeKey: false
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.reload();
    }
  });
}


// Function to show marketplace Chats
function loadMarketplaceChats() {
  chrome.runtime.sendMessage({
    action: 'mrktPlcChatLoadingWait'
  })
  var marketplaceChats = $(`
    ${selectors.grid.container} 
    ${selectors.grid.cell}
    ${selectors.grid.button} 
    ${selectors.svg.mrktPlc}
    `);
  if (marketplaceChats.length) {
    setTimeout(() => {
      try {
        marketplaceChats[0].closest(`${selectors.grid.button}`).click();
        chrome.runtime.sendMessage({
          action: "loadingMarketplaceChats"
        });
      } catch (error) {
        console.error("Error clicking marketplace chat:", error);
        chrome.runtime.sendMessage({
          action: "clickError",
          error: error.message
        });
        chrome.runtime.sendMessage({
          action: 'noMarketplaceFound'
        })
      }
    }, 2000);
  } else {
    chrome.runtime.sendMessage({
      action: "noMarketplaceFound"
    });
  }
}

const PATTERNS = [
  "MarketPlace", "Mark", "place", "mark", "marketplace",
  "Marketplace", "ຕະຫຼາດ", "වෙළඳපොළ", "Marketplace", "بازار",
  "Շուկա", "Tregu", "Pamusika", "Tirgus", "Firoşgeh",
  "Tranzaksyon", "Mercado", "Merke", "Sølutorg",
  "Azoka", "Bazaro", "Goobta suuqa"
];

// Function to start marketplace deletion
function startMarketplaceDeletion() {
  if (isMarketplaceChatsDeletionStopped) {
    return;
  }
  const regexPattern = new RegExp(PATTERNS.join('|'), 'i');
  const marketplaceChatContainer = $('div[role="grid"][aria-label]').filter(function () {
    return regexPattern.test($(this).attr('aria-label'));
  });
  const eachMarketplaceChat = marketplaceChatContainer.find(`
    ${selectors.grid.cell} 
    ${selectors.grid.button}
    ${selectors.svg.menuDots}
    `);
  if (eachMarketplaceChat.length) {
    eachMarketplaceChat[0].closest(selectors.grid.button).click();
    mrktIntvl1 = setInterval(function () {
      const menuMarketplaceDeleteBtn = $(`
        ${selectors.menu.menu}
        ${selectors.menu.item}
        ${selectors.svg.deleteChat}
        `);
      if (menuMarketplaceDeleteBtn.length) {
        menuMarketplaceDeleteBtn[0].closest(selectors.menu.item).click();
        clearInterval(mrktIntvl1);
        mrktIntvl2 = setInterval(function () {
          const confirmMrktDeletionButton = $(selectors.dialog.confirmButton);
          if (confirmMrktDeletionButton.length) {
            confirmMrktDeletionButton[0].click();
            clearInterval(mrktIntvl2);
            mrktCount++;
            showingMrktPlcMsg();
            setTimeout(() => {
              startMarketplaceDeletion();
            }, 1000);
          }
        }, 500);
      }
    }, 500);


  } else {
    isMarketplaceChatsDeletionStopped = true;
    console.log("All Deleted / No marketplace chats found.");
    Swal.fire({
      title: 'MarketPlace Chats',
      text: 'All Deleted / No marketplace chats.',
      icon: 'info'
    });
    chrome.runtime.sendMessage({
      action: 'deletionMarketplaceCompleted'
    });
  }
}

function showingMrktPlcMsg() {
  chrome.runtime.sendMessage({
    action: "trialsLimit",
    count: mrktCount
  });
  chrome.runtime.sendMessage({
    action: "deletionMarketplaceProgressCompleted",
    marketplaceProgress: mrktCount
  });
}

// Function to stop marketplace deletion
function stopMarketplaceDeletion() {
  clearInterval(mrktIntvl1);
  clearInterval(mrktIntvl2);
  isMarketplaceChatsDeletionStopped = true;
  chrome.runtime.sendMessage({
    action: 'deletionMarketplaceCompleted'
  });
  Swal.fire({
    title: 'Stopped',
    text: 'You can restart deletion after page reload.',
    icon: 'warning',
    confirmButtonText: 'OK',
    allowOutsideClick: false,
    allowEscapeKey: false
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.reload();
    }
  });
}

// WARNING: The patterns listed in this array are proprietary and original.
// Unauthorized use, copying, or distribution of these patterns without permission is prohibited.

const PATTERNS2 = [
  "Archive chat",
  "Archive chat",
  "Archive chat",
  "Archive chat",
  "Archive chat",
  "Archive chat",
  "Archi",
  "Archiv",
  "Arch",
  "Archiver la discussion",
  "Archivar chat",
  "Archive chat",
  "Chat archivieren",
  "Arsipkan Obrolan",
  "Arkib Sembang",
  "Arsipkan Obrolan",
  "Archivovat chat",
  "Arkivér chat",
  "Discussion archivée",
  "Arhiviranje razgovora",
  "Archivia chat",
  "Chat archiválása",
  "Arkiver chat",
  "Zarchiwizuj czat",
  "Arquivar bate-papo",
  "Arquivar conversa",
  "Arhivează conversaţia",
  "Archivovať čet",
  "Arkistoi keskustelu",
  "Arkivera chatt",
  "Lưu trữ đoạn chat",
  "Sohbeti Arşivle",
  "Chat archiveren",
  "Αρχειοθέτηση συνομιλίας",
  "Архивировать чат",
  "העברת צ'אט לארכיון",
  "أرشفة الدردشة",
  "चैट आर्काइव करें",
  "チャットをアーカイブ",
  "封存聊天室",
  "채팅 보관",
  "จัดเก็บแชท",
  "ചാറ്റ് ആർക്കൈവുചെയ്യുക",
  "ಚಾಟ್ ಅನ್ನು ಆರ್ಕೈವ್ ಮಾಡಿ",
  "ఆర్కైవ్ చాట్",
  "அரட்டையைக் காப்பகப்படுத்தவும்",
  "ચેટ આર્કાઇવ કરો",
  "চ্যাট আর্কাইভ করুন"
];


function startArchive() {
  if (isArchiveStopped) return;
  const eachChat = $(`
    ${selectors.grid.container} 
    ${selectors.grid.cell} 
    ${selectors.grid.button}
    ${selectors.svg.menuDots}
    `);
  if (eachChat.length) {
    eachChat.first().closest(selectors.grid.button).click();
    const regexPattern = new RegExp(PATTERNS2.join('|'), 'i');
    archivInt1 = setInterval(() => {
      const menuItems = document.querySelectorAll(`${selectors.menu.menu} ${selectors.menu.item} span`);
      for (const span of menuItems) {
        const spanText = span.textContent || span.innerText;
        if (regexPattern.test(spanText)) {
          span.closest(selectors.menu.item).click();
          clearInterval(archivInt1);
          archivCount++;
          showingArchiveMsg();
          setTimeout(() => { startArchive() }, 1000);
        }
      }
    }, 500);
  } else {
    isArchiveStopped = true;
    Swal.fire({
      title: 'Archive Messages',
      text: 'All Archived/ No messages.',
      icon: 'info'
    });
    chrome.runtime.sendMessage({
      action: 'archiveCompleted'
    });
  }
}

function showingArchiveMsg() {
  chrome.runtime.sendMessage({
    action: "trialsLimit",
    count: archivCount
  });
  chrome.runtime.sendMessage({
    action: "archiveProgressCompleted",
    archiveProgress: archivCount
  });
}

function stopArchive() {
  isArchiveStopped = true;
  clearInterval(archivInt1);
  chrome.runtime.sendMessage({
    action: 'archiveCompleted'
  });
  Swal.fire({
    title: 'Stopped',
    text: 'You can restart archive msgs after page reload.',
    icon: 'warning',
    confirmButtonText: 'OK',
    allowOutsideClick: false,
    allowEscapeKey: false
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.reload();
    }
  });
}





