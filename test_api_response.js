const axios = require('axios');

// ID of the chat we want to test
const SESSION_ID = "66277016-074e-4042-8c73-cffac308bed8";

async function testApiResponse() {
  try {
    console.log(`Testing API response for chat ${SESSION_ID}`);
    
    const response = await axios.get(`http://127.0.0.1:5000/api/chat/${SESSION_ID}`);
    const data = response.data;
    
    console.log('\n--- API RESPONSE SUMMARY ---');
    console.log(`Session ID: ${data.session_id}`);
    console.log(`Project: ${data.project?.name}`);
    console.log(`Total messages: ${data.messages?.length || 0}`);
    
    // Check for code blocks
    let messagesWithCodeBlocks = 0;
    let totalCodeBlocks = 0;
    
    if (data.messages && Array.isArray(data.messages)) {
      data.messages.forEach((msg, i) => {
        const hasCodeBlocks = msg.codeBlocks && Array.isArray(msg.codeBlocks) && msg.codeBlocks.length > 0;
        if (hasCodeBlocks) {
          messagesWithCodeBlocks++;
          totalCodeBlocks += msg.codeBlocks.length;
          
          console.log(`\nMessage ${i} (${msg.role}):`);
          console.log(`- Content length: ${msg.content ? msg.content.length : 0} chars`);
          console.log(`- Code blocks: ${msg.codeBlocks.length}`);
          
          // Show details for each code block
          msg.codeBlocks.forEach((block, j) => {
            console.log(`  Code block ${j}:`);
            console.log(`  - Language: ${block.language || 'none'}`);
            console.log(`  - Content length: ${block.content ? block.content.length : 0} chars`);
            console.log(`  - First line: ${block.content ? block.content.split('\n')[0].substring(0, 40) + '...' : 'N/A'}`);
          });
        }
      });
    }
    
    console.log('\n--- SUMMARY ---');
    console.log(`Messages with code blocks: ${messagesWithCodeBlocks} out of ${data.messages?.length || 0}`);
    console.log(`Total code blocks: ${totalCodeBlocks}`);
    
    // Log the shape of a message to understand its structure
    if (data.messages && data.messages.length > 0) {
      const sampleMsg = data.messages.find(msg => msg.codeBlocks && msg.codeBlocks.length > 0) || data.messages[0];
      console.log('\nSample message structure:');
      console.log(JSON.stringify(sampleMsg, null, 2));
    }
    
  } catch (error) {
    console.error('Error testing API response:', error.message);
    if (error.response) {
      console.error('API error status:', error.response.status);
      console.error('API error data:', error.response.data);
    }
  }
}

testApiResponse(); 