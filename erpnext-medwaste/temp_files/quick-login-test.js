const puppeteer = require('puppeteer');

async function quickLoginTest() {
    console.log('🔐 Quick ERPNext login test...');
    
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: { width: 1280, height: 720 }
    });

    try {
        const page = await browser.newPage();
        page.setDefaultTimeout(45000);
        
        console.log('📍 Navigating to login page...');
        await page.goto('http://localhost', { waitUntil: 'domcontentloaded' });
        
        // Wait for and clear the email field
        await page.waitForSelector('input[data-fieldname="usr"]', { timeout: 10000 });
        await page.click('input[data-fieldname="usr"]', { clickCount: 3 });
        await page.type('input[data-fieldname="usr"]', 'Administrator');
        
        // Enter password
        await page.type('input[data-fieldname="pwd"]', 'admin123');
        
        console.log('✅ Credentials entered, attempting login...');
        
        // Click login and wait with a longer timeout
        await page.click('button[type="submit"]');
        
        // Wait for redirect to dashboard/desktop
        try {
            await page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 });
            
            const url = page.url();
            console.log(`✅ Login successful! Current URL: ${url}`);
            
            // Take screenshot of logged in state
            await page.screenshot({ path: 'logged-in-dashboard.png', fullPage: true });
            console.log('📸 Dashboard screenshot saved');
            
            // Wait a bit for the page to fully load
            await page.waitForTimeout(3000);
            
            // Check for ERPNext elements
            const workspaceElements = await page.$$('[data-label*="workspace"], .workspace-container, .dashboard-graph');
            console.log(`📊 Found ${workspaceElements.length} workspace/dashboard elements`);
            
            if (workspaceElements.length > 0) {
                console.log('✅ ERPNext dashboard loaded successfully');
            }
            
        } catch (navError) {
            console.log('⚠️ Navigation timeout, but login may have succeeded');
            const currentUrl = page.url();
            if (!currentUrl.includes('login')) {
                console.log('✅ Not on login page anymore - login likely successful');
                await page.screenshot({ path: 'post-login-state.png', fullPage: true });
            }
        }
        
    } catch (error) {
        console.error('❌ Test error:', error.message);
        await page.screenshot({ path: 'login-error.png', fullPage: true });
    } finally {
        setTimeout(() => browser.close(), 5000); // Keep browser open for 5 seconds
        console.log('🔚 Test completed');
    }
}

quickLoginTest().catch(console.error);