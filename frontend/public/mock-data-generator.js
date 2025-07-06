/**
 * Frontend mock data generator - Run this in browser console
 * This script generates mock tickets using the frontend API client
 */

// Mock ticket templates for testing
const TICKET_TEMPLATES = [
  {
    name: "Login authentication failing",
    description: "Users cannot authenticate due to session timeout issues. The authentication service is returning unexpected errors.",
    error_message: "SessionTimeoutException: User session expired after 30 minutes",
    keywords: ["auth", "session", "timeout", "login"]
  },
  {
    name: "React component rendering error",
    description: "Dashboard components are not rendering properly after the latest update. White screen appears instead of charts.",
    error_message: "TypeError: Cannot read properties of undefined (reading 'map') at Dashboard.tsx:45",
    keywords: ["react", "component", "rendering", "dashboard", "frontend"]
  },
  {
    name: "Database query performance issue",
    description: "User profile queries are taking more than 10 seconds to complete. Database performance has degraded significantly.",
    error_message: "QueryTimeoutException: Query execution time exceeded 10000ms",
    keywords: ["database", "performance", "query", "timeout"]
  },
  {
    name: "API endpoint returning 502 errors",
    description: "The user management API is consistently returning 502 Bad Gateway errors. Load balancer might be misconfigured.",
    error_message: "502 Bad Gateway: upstream server timeout",
    keywords: ["api", "502", "gateway", "timeout", "server"]
  },
  {
    name: "Mobile app push notifications not working",
    description: "Push notifications are not being delivered to mobile devices. Firebase configuration might be incorrect.",
    error_message: "Firebase messaging error: Invalid registration token",
    keywords: ["mobile", "push", "notifications", "firebase"]
  },
  {
    name: "File upload size limit exceeded",
    description: "Users cannot upload files larger than 5MB. The upload process fails without proper error messaging.",
    error_message: "PayloadTooLargeError: File size exceeds maximum allowed size of 5MB",
    keywords: ["upload", "file", "size", "limit", "error"]
  },
  {
    name: "Cache invalidation not working",
    description: "User data is not being updated in real-time. Cache invalidation appears to be broken.",
    error_message: "Redis cache invalidation failed: Connection refused",
    keywords: ["cache", "redis", "invalidation", "real-time"]
  },
  {
    name: "SSL certificate validation error",
    description: "HTTPS requests are failing due to SSL certificate validation issues. Certificate might be expired.",
    error_message: "SSL Error: Certificate has expired on api.example.com",
    keywords: ["ssl", "certificate", "https", "expired", "security"]
  }
];

// Function to generate a random ticket
function generateRandomTicket() {
  const template = TICKET_TEMPLATES[Math.floor(Math.random() * TICKET_TEMPLATES.length)];
  const ticketNumber = Math.floor(Math.random() * 1000) + 1;
  
  return {
    name: `${template.name} #${ticketNumber}`,
    description: template.description,
    error_message: template.error_message,
    keywords: [...template.keywords, `issue-${ticketNumber}`],
    screenshot_url: Math.random() < 0.3 ? `https://example.com/screenshots/issue-${ticketNumber}.png` : undefined
  };
}

// Function to create multiple tickets
async function createMockTickets(count = 10) {
  console.log(`🚀 Creating ${count} mock tickets...`);
  
  // Check if ticketAssistantAPI is available
  if (typeof ticketAssistantAPI === 'undefined') {
    console.error('❌ ticketAssistantAPI not found. Make sure you are on a page where the API client is loaded.');
    return;
  }
  
  const results = [];
  
  for (let i = 0; i < count; i++) {
    try {
      const ticketData = generateRandomTicket();
      console.log(`📝 Creating ticket ${i + 1}/${count}: ${ticketData.name}`);
      
      // Use the combined endpoint to create ticket with classification
      const result = await ticketAssistantAPI.submitTicketWithClassificationMock(ticketData);
      
      console.log(`   ✅ Created: ${result.ticket.id} [${result.classification.department.toUpperCase()}/${result.classification.severity.toUpperCase()}]`);
      results.push(result);
      
      // Small delay between requests
      await new Promise(resolve => setTimeout(resolve, 200));
      
    } catch (error) {
      console.error(`   ❌ Failed to create ticket ${i + 1}:`, error);
    }
  }
  
  console.log(`\n🎉 Mock data generation complete!`);
  console.log(`✅ Successfully created ${results.length} tickets`);
  
  // Show summary
  if (results.length > 0) {
    console.log('\n📊 Department distribution:');
    const deptCounts = {};
    results.forEach(r => {
      const dept = r.classification.department;
      deptCounts[dept] = (deptCounts[dept] || 0) + 1;
    });
    Object.entries(deptCounts).forEach(([dept, count]) => {
      console.log(`   ${dept.toUpperCase()}: ${count} tickets`);
    });
    
    console.log('\n⚠️ Severity distribution:');
    const severityCounts = {};
    results.forEach(r => {
      const severity = r.classification.severity;
      severityCounts[severity] = (severityCounts[severity] || 0) + 1;
    });
    Object.entries(severityCounts).forEach(([severity, count]) => {
      console.log(`   ${severity.toUpperCase()}: ${count} tickets`);
    });
  }
  
  // Trigger dashboard refresh
  console.log('\n🔄 Triggering dashboard refresh...');
  window.dispatchEvent(new CustomEvent('ticketCreated', { 
    detail: { 
      message: `${results.length} mock tickets created`,
      count: results.length 
    } 
  }));
  
  return results;
}

// Function to quickly create a single test ticket
async function createTestTicket() {
  const ticketData = generateRandomTicket();
  console.log('🧪 Creating test ticket:', ticketData.name);
  
  try {
    const result = await ticketAssistantAPI.submitTicketWithClassificationMock(ticketData);
    console.log('✅ Test ticket created:', result);
    
    // Trigger dashboard refresh
    window.dispatchEvent(new CustomEvent('ticketCreated', { detail: result }));
    
    return result;
  } catch (error) {
    console.error('❌ Failed to create test ticket:', error);
    throw error;
  }
}

// Export functions to global scope for console use
window.createMockTickets = createMockTickets;
window.createTestTicket = createTestTicket;

console.log('🎯 Mock data generator loaded!');
console.log('📝 Usage:');
console.log('   createMockTickets(10)  // Create 10 mock tickets');
console.log('   createTestTicket()     // Create 1 test ticket');
console.log('   createMockTickets(50)  // Create 50 mock tickets');
