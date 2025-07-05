#!/usr/bin/env node

/**
 * Frontend Status Check
 * Verifies that the frontend is properly configured and running
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Ticket Assistant Frontend - Status Check');
console.log('==========================================');

// Check if we're in the right directory
const packageJsonPath = path.join(process.cwd(), 'package.json');
if (!fs.existsSync(packageJsonPath)) {
  console.log('❌ package.json not found. Are you in the frontend directory?');
  process.exit(1);
}

const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
console.log(`✅ Project: ${packageJson.name}`);
console.log(`✅ Version: ${packageJson.version}`);

// Check key files
const keyFiles = [
  'src/App.tsx',
  'src/main.tsx',
  'src/router.tsx',
  'src/pages/Dashboard.tsx',
  'src/pages/TicketSubmission.tsx',
  'src/pages/TicketList.tsx',
  'src/pages/TicketDetails.tsx',
  'src/pages/Reports.tsx',
  'src/lib/api/client.ts',
  'tailwind.config.js',
  'vite.config.ts'
];

let allFilesExist = true;
keyFiles.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - Missing`);
    allFilesExist = false;
  }
});

if (allFilesExist) {
  console.log('\n🎉 All key files are present!');
} else {
  console.log('\n⚠️ Some files are missing. Please check your setup.');
}

// Check node_modules
if (fs.existsSync('node_modules')) {
  console.log('✅ node_modules directory exists');
} else {
  console.log('❌ node_modules directory missing. Run: npm install');
}

// Check if build dist exists
if (fs.existsSync('dist')) {
  console.log('✅ dist directory exists (build has been run)');
} else {
  console.log('ℹ️ dist directory not found (build not run yet)');
}

console.log('\n📋 Environment Information:');
console.log(`Node.js: ${process.version}`);
console.log(`Platform: ${process.platform}`);
console.log(`Architecture: ${process.arch}`);

console.log('\n🚀 To start the development server:');
console.log('   npm run dev');
console.log('   or directly: ./node_modules/.bin/vite');

console.log('\n🌐 Expected URLs:');
console.log('   Development: http://localhost:5173');
console.log('   Alternative: http://localhost:3000');

console.log('\n📝 Available routes:');
console.log('   / - Dashboard');
console.log('   /submit - Submit Ticket');
console.log('   /tickets - All Tickets');
console.log('   /tickets/:id - Ticket Details');
console.log('   /reports - Reports & Analytics');
