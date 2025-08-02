import { KEYBOARD_COMMANDS, RUNTIME_MESSAGES } from "./constants";

chrome.commands.onCommand.addListener((command) => {
  chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
    if (!tab?.id) return;

    switch (command) {
      case KEYBOARD_COMMANDS.TOGGLE_SIDE_PANEL:
        chrome.sidePanel.open({ tabId: tab.id });
        break;

      case KEYBOARD_COMMANDS.ADD_TO_OBSIDIZER:
        chrome.sidePanel.open({ tabId: tab.id });
        chrome.scripting.executeScript(
          {
            target: { tabId: tab.id },
            func: () => {
              try {
                return window?.getSelection?.()?.toString?.() || "";
              } catch (e) {
                return e;
              }
            },
          },
          (results) => {
            if (!tab?.id) return;
            chrome.runtime.sendMessage({
              type: RUNTIME_MESSAGES.ADD_TO_OBSIDIZER,
              text: results?.[0]?.result || "",
              id: Date.now(),
            });
          }
        );
        break;
    }
  });
});
