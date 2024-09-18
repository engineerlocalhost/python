var app = angular.module("myapp", []);

app.controller("ctrl", function ($scope, $http, $timeout, $window) {
  $scope.showNotOnFacebookMsg = true;
  $scope.showGoToFBMessangerButton = true;
  $scope.showMainPage = false;
  $scope.messengerDeletionInProgress = false;
  $scope.marketplaceDeletionInProgress = false;
  $scope.archiveInProgress = false;
  $scope.showStartArchiveButton = true;
  $scope.activeTab = 'messengerTab';
  $scope.showStartDeletionButton = true;
  $scope.showSuccessMessage = false;
  $scope.deletionProgress = 0;
  $scope.showStartMarketplaceDeletionButton = false;
  $scope.showLoadMarketplaceChatsButton = true;
  $scope.showWarningMessageNoMarketplace = false;
  $scope.marketplaceDeletionProgress = 0;
  $scope.archiveProgress = 0;
  //$scope.trialsCount = 0;
  // $scope.trialsLimitComplete = false;
  //$scope.license = false;
 // $scope.trialsUpdateCount = 0;
  $scope.mrktPlcChatLoadingWait = false;
  $scope.loadingCureentTabinfo = false;
  $scope.encodedT = 'NQ==';
  $scope.decodedT = parseInt(atob($scope.encodedT));



  // Function to handle tab content transitions
  $scope.handleTabTransition = function (tabId) {
    var allTabs = document.querySelectorAll('.tab-pane');
    allTabs.forEach(function (tab) {
      tab.classList.remove('active');
    });
    var tabContent = document.getElementById(tabId);
    setTimeout(function () {
      tabContent.classList.add('active');
    }, 10);
  };

  // Initialize the state based on whether chats are already loaded or deletions are in progress
  //chrome.storage.sync.get(['marketplaceChatsLoaded', 'messengerDeletionInProgress', 'marketplaceDeletionInProgress', 'archiveInProgress'], function (result) {
    //$scope.$apply(function () {
      //Handle marketplace chat buttons
      //$scope.showLoadMarketplaceChatsButton = !result.marketplaceChatsLoaded;
     // $scope.showStartMarketplaceDeletionButton = result.marketplaceChatsLoaded && !result.marketplaceDeletionInProgress;
     // $scope.marketplaceDeletionInProgress = result.marketplaceDeletionInProgress || false;
      

      // Handle messenger deletion button
  //     if (result.messengerDeletionInProgress) {
  //       $scope.messengerDeletionInProgress = true;
  //       $scope.showStartDeletionButton = false;
  //     } else {
  //       $scope.messengerDeletionInProgress = false;
  //       $scope.showStartDeletionButton = true;
  //     }
  //      if (result.archiveInProgress) {
  //       $scope.showStartArchiveButton = false;
  //       $scope.archiveInProgress = true;
  //      } else {
  //       $scope.showStartArchiveButton = true;
  //       $scope.archiveInProgress = false;
  //      }
  //   });
  // });

  $scope.activeTab = $window.localStorage.getItem('activeTab') || 'messengerTab'; // Default to 'messengerTab'

  // Function to switch tabs and save the state
  $scope.switchTab = function (tabId) {
    $scope.activeTab = tabId;
    $window.localStorage.setItem('activeTab', tabId);
  };

  // Function to check if a tab is active
  $scope.isTabActive = function (tabId) {
    return $scope.activeTab === tabId;
  };

  $scope.goToFBMessanger = function () {
    chrome.tabs.create({
      url: 'https://www.facebook.com/messages/'
    });
  };

  $scope.startMessengerDeletion = function () {
    if ($scope.trialsLimitComplete && !$scope.license) {
      console.log("Trial limit reached. Please purchase a license.");
      return;
    }

    $scope.messengerDeletionInProgress = true;
    $scope.showStartDeletionButton = false;
    $scope.showSuccessMessage = false;
    $scope.deletionProgress = 0;

    chrome.storage.sync.set({
      messengerDeletionInProgress: true
    });

    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      var activeTab = tabs[0];
      if (activeTab.url.match(/facebook.com\/messages|facebook.com\/latest\/inbox/i)) {
        chrome.tabs.sendMessage(activeTab.id, {
          action: 'startChatsDeletion'
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError.message);
          } else {
            console.log(response.status);
          }
        });
      } else {
        console.log("You are not on the Facebook Messenger page.");
      }
    });
  };

  $scope.stopMessengerDeletion = function () {
    $scope.messengerDeletionInProgress = false;

    chrome.storage.sync.set({
      messengerDeletionInProgress: false
    });

    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      var activeTab = tabs[0];
      if (activeTab.url.match(/facebook.com\/messages|facebook.com\/latest\/inbox/i)) {
        chrome.tabs.sendMessage(activeTab.id, {
          action: "stopChatsDeletion"
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError.message);
          } else {
            console.log(response.status);
          }
        });
      }
    });

  //   $timeout(function () {
  //     //$scope.showStartDeletionButton = true;
  //     $scope.showSuccessMessage = true;
  //   }, 500); // Delay to show transition
  // };

  $scope.loadMarketplaceChats = function () {
    $scope.showLoadMarketplaceChatsButton = false;
    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {
        action: "loadMarketplaceChats"
      }, function (response) {
        if (response && response.status === "success") {
          chrome.storage.sync.set({
            marketplaceChatsLoaded: true
          }, function () {
            $scope.$apply(function () {
              //$scope.showLoadMarketplaceChatsButton = false;
              //$scope.showStartMarketplaceDeletionButton = true;
              //$scope.showWarningMessageNoMarketplace = false; // Reset warning message
            });
          });
        }
      });
    });
  };

  $scope.startMarketplaceDeletion = function () {
    if ($scope.trialsLimitComplete && !$scope.license) {
      console.log("Trial limit reached. Please purchase a license.");
      return;
    }

    //$scope.marketplaceDeletionInProgress = true;
    //$scope.showStartMarketplaceDeletionButton = false;
    //$scope.marketplaceDeletionProgress = 0;

    chrome.storage.sync.set({
      marketplaceDeletionInProgress: true
    });

    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      var activeTab = tabs[0];
      if (activeTab.url.match(/facebook.com\/messages|facebook.com\/latest\/inbox/i)) {
        chrome.tabs.sendMessage(activeTab.id, {
          action: "startMarketplaceDeletion"
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError);
          } else {
            console.log(response.status);
          }
        });
      }
    });
  };

  $scope.stopMarketplaceDeletion = function () {
    $scope.marketplaceDeletionInProgress = false;
    chrome.storage.sync.set({
      marketplaceDeletionInProgress: false
    });

    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      var activeTab = tabs[0];
      if (activeTab.url.match(/facebook.com\/messages|facebook.com\/latest\/inbox/i)) {
        chrome.tabs.sendMessage(activeTab.id, {
          action: "stopMarketplaceDeletion"
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError.message);
          } else {
            console.log(response.status);
          }
        });
      }
    });
  };

  // $scope.startArchive = function () {
  //   if ($scope.trialsLimitComplete && !$scope.license) {
  //     console.log("Trial limit reached. Please purchase a license.");
  //     return;
  //   }

    $scope.archiveInProgress = true;
    $scope.showStartArchiveButton = false;
    $scope.archiveProgress = 0;

    chrome.storage.sync.set({
      archiveInProgress: true
    });

    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      var activeTab = tabs[0];
      if (activeTab.url.match(/facebook.com\/messages|facebook.com\/latest\/inbox/i)) {
        chrome.tabs.sendMessage(activeTab.id, {
          action: 'startArchive'
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError.message);
          } else {
            console.log(response.status);
          }
        });
      } else {
        console.log("You are not on the Facebook Messenger page.");
      }
    });
  };

  $scope.stopArchive = function () {
    $scope.archiveInProgress = false;

    chrome.storage.sync.set({
      archiveInProgress: false
    });

    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      var activeTab = tabs[0];
      if (activeTab.url.match(/facebook.com\/messages|facebook.com\/latest\/inbox/i)) {
        chrome.tabs.sendMessage(activeTab.id, {
          action: "stopArchive"
        }, function (response) {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError.message);
          } else {
            console.log(response.status);
          }
        });
      }
    });


    $scope.showStartArchiveButton = true;

  };

  $scope.loadMarketplaceChats = function () {
    $scope.showLoadMarketplaceChatsButton = false;
    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {
        action: "loadMarketplaceChats"
      }, function (response) {
        if (response && response.status === "success") {
          chrome.storage.sync.set({
            marketplaceChatsLoaded: true
          }, function () {
             $scope.$apply(function () {
              $scope.showLoadMarketplaceChatsButton = false;
              $scope.showStartMarketplaceDeletionButton = true;
               $scope.showWarningMessageNoMarketplace = false; // Reset warning message
          });
          });
        }
      });
    });
  };


  $scope.checkCurrentTab = function () {
    $scope.loadingCureentTabinfo = true;
    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, function (tabs) {
      var activeTab = tabs[0];
      var tabUpdateListener;
      chrome.tabs.onUpdated.removeListener(tabUpdateListener);
      if (activeTab.url.match(/facebook.com\/messages|facebook.com\/latest\/inbox/i)) {
        chrome.tabs.get(activeTab.id, function (tab) {
          if (tab.status === 'complete') {
            $scope.$apply(function () {
              $scope.showNotOnFacebookMsg = false;
              $scope.showGoToFBMessangerButton = false;
              $scope.showMainPage = true; // Show the main page
              $scope.loadingCureentTabinfo = false; // Hide loading indicator
            });
          } else {
            $scope.$apply(function () {
              $scope.showNotOnFacebookMsg = false;
              $scope.showGoToFBMessangerButton = false;
              $scope.showMainPage = false; // Initially hide the main page
              $scope.loadingCureentTabinfo = true; // Show loading indicator
            });

            // Listener for when the tab finishes loading
            tabUpdateListener = function (tabId, changeInfo, tab) {
              if (tabId === activeTab.id && changeInfo.status === 'complete') {
                $scope.$apply(function () {
                  $scope.showNotOnFacebookMsg = false;
                  $scope.showGoToFBMessangerButton = false;
                  $scope.showMainPage = true; // Show the main page
                  $scope.loadingCureentTabinfo = false; // Hide loading indicator
                });
                chrome.tabs.onUpdated.removeListener(tabUpdateListener); // Clean up listener
              }
            };

            chrome.tabs.onUpdated.addListener(tabUpdateListener);
          }
        });
      } else {
        chrome.storage.sync.set({
          marketplaceChatsLoaded: false,
          messengerDeletionInProgress: false,
          marketplaceDeletionInProgress: false
        });
        $scope.$apply(function () {
          $scope.showNotOnFacebookMsg = true;
          $scope.showGoToFBMessangerButton = true;
          $scope.showMainPage = false;
          $scope.loadingCureentTabinfo = false;
        });
      }
    });
  };

  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === 'deletionCompleted') {
      $scope.$apply(function () {
        $scope.messengerDeletionInProgress = false;
        $scope.showSuccessMessage = true; // Show success message if needed

        $timeout(function () {
          $scope.showStartDeletionButton = true;
        }, 500); // Delay to show transition
      });

      chrome.storage.sync.set({
        messengerDeletionInProgress: false
      });
    } else if (request.action === 'deletionProgress') {
      $scope.$apply(function () {
        $scope.deletionProgress = request.progress;
      });
    } else if (request.action === "mrktPlcChatLoadingWait") {
      $scope.$apply(function () {
        $scope.mrktPlcChatLoadingWait = true;
      });
    } else if (request.action === "loadingMarketplaceChats") {
      $scope.$apply(function () {
        $scope.mrktPlcChatLoadingWait = false;
        $scope.showLoadMarketplaceChatsButton = false;
        $scope.showStartMarketplaceDeletionButton = true;
        $scope.showWarningMessageNoMarketplace = false;
      });
      chrome.storage.sync.set({
        marketplaceChatsLoaded: true
      });
    } else if (request.action === 'backButtonClicked') {
      $scope.$apply(function () {
        $scope.mrktPlcChatLoadingWait = false;
        $scope.showLoadMarketplaceChatsButton = true;
        $scope.showStartMarketplaceDeletionButton = false;
        $scope.showWarningMessageNoMarketplace = false;
        chrome.storage.sync.set({
          marketplaceChatsLoaded: false
        });
      });
    } else if (request.action === "noMarketplaceFound") {
      $scope.$apply(function () {
        $scope.mrktPlcChatLoadingWait = false;
        $scope.showLoadMarketplaceChatsButton = false;
        $scope.showStartMarketplaceDeletionButton = false;
        $scope.showWarningMessageNoMarketplace = true;
        $timeout(function () {
          $scope.mrktPlcChatLoadingWait = false;
          $scope.showWarningMessageNoMarketplace = false;
          $scope.showLoadMarketplaceChatsButton = true;
        }, 2000);
      });
      chrome.storage.sync.set({
        marketplaceChatsLoaded: false
      });
    } else if (request.action === "deletionMarketplaceCompleted") {
      $scope.$apply(function () {
        $scope.marketplaceDeletionInProgress = false;
        $timeout(function () {
          $scope.showStartMarketplaceDeletionButton = true;
        }, 500);
      });
      chrome.storage.sync.set({
        marketplaceChatsLoaded: false,
        marketplaceDeletionInProgress: false
      });
    } else if (request.action === 'deletionMarketplaceProgressCompleted') {
      $scope.$apply(function () {
        $scope.marketplaceDeletionProgress = request.marketplaceProgress;
      });
    } else if (request.action === "trialsLimit") {
      $scope.$apply(function () {
        $scope.trialsCount = request.count;
        console.log($scope.trialsCount);
      });
      //$scope.useTrial();
      //$scope.trialsUpdateCount++;
      //console.log("Trials updation count : ", $scope.trialsUpdateCount);
    } else if (request.action === 'archiveCompleted') {
      $scope.$apply(() => {
        $scope.archiveInProgress = false;
        $scope.showStartArchiveButton = true;
        chrome.storage.sync.set({
          archiveInProgress: false
        });
      });
    } else if (request.action === 'archiveProgressCompleted') {
      $scope.$apply(() => {
        $scope.archiveProgress = request.archiveProgress;
      });
    }
  });

  $scope.checkCurrentTab();

  // $scope.useTrial = function () {
  //   chrome.storage.sync.get(['trialsCount'], function (result) {
  //     // Ensure the trials count is always updated and checked
  //     const storedTrialsCount = result.trialsCount || 0;
  //     const newTrialsCount = storedTrialsCount + 1;

  //     chrome.storage.sync.set({
  //       trialsCount: newTrialsCount
  //     }, function () {
  //       $scope.trialsUpdateCount = newTrialsCount;
  //       $scope.checkTrials();
  //     });
  //   });
  // };

  // $scope.checkTrials = function () {
  //   chrome.storage.sync.get(['trialsCount'], function (result) {
  //     const storedTrialsCount = result.trialsCount || 0;
  //     if (storedTrialsCount >= $scope.decodedT && !$scope.license) {
  //       $scope.stopMessengerDeletion();
  //       $scope.stopMarketplaceDeletion();
  //       $scope.stopArchive();
  //       chrome.storage.sync.set({
  //         trialsLimitComplete: false
  //       });
  //       $scope.$apply(function () {
  //         $scope.trialsLimitComplete = false;
  //         toastr.info('Your free trial has ended. Please purchase a subscription to continue with unlimited deletion access.');
  //       });
  //     }
  //   });
  // };


  // chrome.storage.sync.get(['trialsLimitComplete'], function (result) {
  //   $scope.$apply(function () {
  //     $scope.trialsLimitComplete = result.trialsLimitComplete || false;
  //   });
  // });

  // var url = "https://api.gumroad.com/v2/licenses/verify";
  // var headers = {
  //   'content-type': 'application/x-www-form-urlencoded'
  // };

  // //$scope.verify_license = function (key) {
  //   if (key) {
  //     $scope.licensebb = true;
  //     $scope.error = false;

  //     $http({
  //       method: "post",
  //       url: url,
  //       data: $.param({
  //         license_key: key,
  //         product_id: "igg8q_nehFMAgmZilxggIg=="
  //       }),
  //       headers: headers,
  //     }).then(function (response) {
  //       $scope.licensebb = false;
  //       if (response.data.success && !response.data.purchase.subscription_cancelled_at && !response.data.purchase.subscription_failed_at) {
  //         $scope.license = true;
  //         chrome.storage.sync.set({
  //           license_key: key
  //         });
  //         toastr.success('Thank you for subscribing! Your license has been successfully validated. Enjoy unlimited deletion capabilities!.', 'Welcome!');
  //         $scope.wlcm = true;
  //         $scope.trialsLimitComplete = false; // Reset the trial limit
  //       } else {
  //         $scope.error = true;
  //         toastr.error('The license key is invalid or the subscription has expired.', 'Error');
  //       }
  //     }, function () {
  //       $scope.licensebb = false;
  //       $scope.error = true;
  //       toastr.error('An error occurred while verifying the license. Please try again.', 'Error');
  //     });
  //   }
  // };

  // chrome.storage.sync.get("license_key", function (result) {
  //   var key = result.license_key;
  //   if (key) {
  //     $scope.$apply(function () {
  //       $scope.license = true;
  //       //$scope.trialsLimitComplete = false;
  //       $http({
  //         method: "post",
  //         url: url,
  //         data: $.param({
  //           license_key: key,
  //           product_id: "igg8q_nehFMAgmZilxggIg=="
  //         }),
  //         headers: headers,
  //       }).then(function (response) {
  //         if (!(response.data.success && !response.data.purchase.subscription_cancelled_at && !response.data.purchase.subscription_failed_at)) {
  //           chrome.storage.sync.set({
  //             license_key: ""
  //           });
  //           $scope.license = false;
  //           $scope.trialsLimitComplete = true;
  //         }
  //       }, function () {
  //         chrome.storage.sync.set({
  //           license_key: ""
  //         });
  //         $scope.license = false;
  //         $scope.trialsLimitComplete = true;
  //       });
  //     });
  //   }
  // });
});
