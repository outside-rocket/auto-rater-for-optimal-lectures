function extractChatData() {
    const chatData = [];

    // Find all message containers using your existing primary selectors
    let messages = document.querySelectorAll('div.message-row');
    if (messages.length === 0) messages = document.querySelectorAll('div.message');
    if (messages.length === 0) messages = document.querySelectorAll('[data-message]');
    if (messages.length === 0) messages = document.querySelectorAll('.msg, .message-item, .chat-message');

    console.log(`Found ${messages.length} messages`);

    messages.forEach((messageEl, index) => {
        try {
            // 1. Target the exact text containers directly
            const textEl = messageEl.querySelector('div.text-content');
            const quotedEl = messageEl.querySelector('div.quoted-content');

            // 2. Extract and clean content only if the elements exist
            let messageContent = textEl ? textEl.textContent.trim().replace(/\s+/g, ' ') : "";
            let context = quotedEl ? quotedEl.textContent.trim().replace(/\s+/g, ' ') : "";

            // Skip empty items
            if (!messageContent && !context) return;

            chatData.push({
                message: messageContent,
                context: context
            });

        } catch (e) {
            console.warn(`Error processing message ${index}:`, e);
        }
    });

    console.log(`\n✓ Extracted ${chatData.length} messages successfully`);

    // Create and download JSON
    const jsonText = JSON.stringify(chatData, null, 2);
    const blob = new Blob([jsonText], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'FFCS_VITC_chat.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    console.log("✓ JSON file downloaded as 'FFCS_VITC_chat.json'");
    return chatData;
}

// Run extraction
extractChatData();