
function timer(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
 
 async function gethtml() {
  await timer(20000);
  chrome.runtime.sendMessage(
    { content: document.documentElement.innerHTML },
    function (response) {
      console.log("success");
    } 
  );
  
}

// setTimeout("gethtml()", 12000); 
gethtml();
  // chrome.runtime.sendMessage(
  //   { content: document.documentElement.innerHTML },
  //   function (response) {
  //     console.log("success");
  //   } 
  // );
 
