function extractStaticChatData() {
    // 1. Verify that the static data container exists on your local HTML file
    if (!window.CHAT_MESSAGES_HTML || !Array.isArray(window.CHAT_MESSAGES_HTML)) {
        console.error("Could not find window.CHAT_MESSAGES_HTML array. Make sure you are running this on the correct file.");
        return;
    }

    const chatData = [];
    const parser = new DOMParser();

    console.log(`Processing ${window.CHAT_MESSAGES_HTML.length} static chat blocks...`);

    // 2. Loop through every raw HTML snippet inside the array
    window.CHAT_MESSAGES_HTML.forEach((htmlString, index) => {
        try {
            // Turn the raw text string into a processable virtual DOM node
            const doc = parser.parseFromString(htmlString, 'text/html');

            // 3. Target your precise text components cleanly
            const textEl = doc.querySelector('div.text-content');
            const quotedEl = doc.querySelector('div.quoted-content');

            // 4. Extract text and clean up whitespace/breaks completely
            let messageContent = textEl ? textEl.textContent.trim().replace(/\s+/g, ' ') : "";
            let context = quotedEl ? quotedEl.textContent.trim().replace(/\s+/g, ' ') : "";

            // Ignore deleted message structures, video items, or empty blocks
            if (!messageContent && !context) return;

            chatData.push({
                message: messageContent,
                context: context
            });

        } catch (e) {
            console.warn(`Error parsing message structure index ${index}:`, e);
        }
    });

    console.log(`\n✓ Successfully parsed and cleaned ${chatData.length} total entries.`);

    // 5. Create and download the finalized JSON block
    const jsonText = JSON.stringify(chatData, null, 2);
    const blob = new Blob([jsonText], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'FFCS_VITC_chat.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    console.log("✓ Final JSON downloaded instantly as 'FFCS_VITC_chat.json'");
    return chatData;
}

// Execute the extraction
extractStaticChatData();