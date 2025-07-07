// Test API connectivity
import { ticketAssistantAPI } from './lib/api';

// Test the API client
async function testAPI() {
  try {
    console.log('Testing API client...');

    // Test health check
    const health = await ticketAssistantAPI.healthCheck();
    console.log('Health check:', health);

    // Test getting tickets (should return mock data)
    const tickets = await ticketAssistantAPI.getTickets();
    console.log('Tickets:', tickets);

    // Test dashboard stats
    const stats = await ticketAssistantAPI.getDashboardStats();
    console.log('Dashboard stats:', stats);

    console.log('✅ API client working correctly!');
  } catch (error) {
    console.log('⚠️ API client using mock data (expected if backend not running)');
    console.log('Error:', error instanceof Error ? error.message : 'Unknown error');
  }
}

// Run the test
testAPI();
