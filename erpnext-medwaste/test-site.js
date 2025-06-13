const puppeteer = require('puppeteer');

async function testERPNextSite() {
    console.log('🚀 Starting ERPNext site test...');
    
    const browser = await puppeteer.launch({
        headless: false, // Set to true for headless testing
        defaultViewport: { width: 1280, height: 720 },
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        
        // Set a reasonable timeout
        page.setDefaultTimeout(30000);
        
        console.log('📍 Navigating to http://localhost...');
        await page.goto('http://localhost', { waitUntil: 'networkidle2' });
        
        // Take a screenshot of the login page
        await page.screenshot({ path: 'login-page.png', fullPage: true });
        console.log('📸 Screenshot saved as login-page.png');
        
        // Check if we're on the login page
        const title = await page.title();
        console.log(`📄 Page title: ${title}`);
        
        // Check for ERPNext elements
        const erpnextBranding = await page.$('.frappe-brand');
        if (erpnextBranding) {
            console.log('✅ ERPNext branding found');
        } else {
            console.log('❌ ERPNext branding not found');
        }
        
        // Check for login form
        const usernameField = await page.$('input[placeholder*="Email"]');
        const passwordField = await page.$('input[type="password"]');
        const loginButton = await page.$('button[type="submit"]');
        
        if (usernameField && passwordField && loginButton) {
            console.log('✅ Login form elements found');
            
            // Test login functionality
            console.log('🔑 Testing login...');
            await page.type('input[placeholder*="Email"]', 'Administrator');
            await page.type('input[type="password"]', 'admin123');
            
            // Take screenshot before login
            await page.screenshot({ path: 'before-login.png' });
            console.log('📸 Before login screenshot saved');
            
            // Click login button
            await Promise.all([
                page.waitForNavigation({ waitUntil: 'networkidle2' }),
                page.click('button[type="submit"]')
            ]);
            
            // Check if login was successful
            const currentUrl = page.url();
            console.log(`📍 Current URL after login: ${currentUrl}`);
            
            if (currentUrl.includes('/app') || currentUrl.includes('desk')) {
                console.log('✅ Login successful - redirected to desktop');
                
                // Take screenshot of the desktop
                await page.screenshot({ path: 'erpnext-desktop.png', fullPage: true });
                console.log('📸 Desktop screenshot saved');
                
                // Check for common ERPNext desktop elements
                const moduleCards = await page.$$('.module-card, .widget, .dashboard-section');
                console.log(`📊 Found ${moduleCards.length} dashboard elements`);
                
                // Check for specific modules
                const modules = ['Stock', 'Manufacturing', 'Buying', 'HR', 'Accounts'];
                for (const module of modules) {
                    const moduleElement = await page.$(`text=${module}`);
                    if (moduleElement) {
                        console.log(`✅ ${module} module found`);
                    } else {
                        console.log(`❌ ${module} module not found`);
                    }
                }
                
                // Test navigation to Stock module (important for medical waste)
                try {
                    await page.click('a[href*="stock"], [data-module="Stock"]');
                    await page.waitForNavigation({ waitUntil: 'networkidle2' });
                    console.log('✅ Successfully navigated to Stock module');
                    
                    await page.screenshot({ path: 'stock-module.png', fullPage: true });
                    console.log('📸 Stock module screenshot saved');
                } catch (error) {
                    console.log('⚠️ Could not navigate to Stock module:', error.message);
                }
                
            } else {
                console.log('❌ Login failed or unexpected redirect');
                const errorMessage = await page.$eval('.alert, .error-message, .msgprint', 
                    el => el.textContent).catch(() => 'No error message found');
                console.log(`Error: ${errorMessage}`);
            }
            
        } else {
            console.log('❌ Login form elements not found');
            console.log(`Username field: ${usernameField ? 'found' : 'not found'}`);
            console.log(`Password field: ${passwordField ? 'found' : 'not found'}`);
            console.log(`Login button: ${loginButton ? 'found' : 'not found'}`);
        }
        
        // Check page performance
        const performanceMetrics = await page.metrics();
        console.log('⚡ Performance metrics:');
        console.log(`  - Layout Duration: ${performanceMetrics.LayoutDuration}ms`);
        console.log(`  - Script Duration: ${performanceMetrics.ScriptDuration}ms`);
        
        console.log('✅ Test completed successfully!');
        
    } catch (error) {
        console.error('❌ Test failed:', error);
        
        // Take error screenshot
        try {
            await page.screenshot({ path: 'error-screenshot.png', fullPage: true });
            console.log('📸 Error screenshot saved');
        } catch (screenshotError) {
            console.log('Could not take error screenshot:', screenshotError.message);
        }
    } finally {
        await browser.close();
        console.log('🔚 Browser closed');
    }
}

// Run the test
testERPNextSite().catch(console.error);