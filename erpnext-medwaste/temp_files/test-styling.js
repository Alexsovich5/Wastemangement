const puppeteer = require('puppeteer');

async function testStyling() {
    console.log('🎨 Testing ERPNext styling...');
    
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: { width: 1280, height: 720 }
    });

    try {
        const page = await browser.newPage();
        
        // Navigate to login page
        console.log('📍 Loading login page...');
        await page.goto('http://localhost', { waitUntil: 'networkidle2' });
        
        // Take screenshot
        await page.screenshot({ path: 'styled-login.png', fullPage: true });
        console.log('📸 Screenshot saved as styled-login.png');
        
        // Check if CSS loaded
        const styles = await page.$$eval('link[rel="stylesheet"]', links => 
            links.map(link => ({
                href: link.href,
                loaded: link.sheet !== null
            }))
        );
        
        console.log('🎨 CSS Files:', styles);
        
        // Check for styled elements
        const hasStyledButton = await page.$eval('button[type="submit"]', btn => {
            const styles = window.getComputedStyle(btn);
            return styles.backgroundColor !== 'rgba(0, 0, 0, 0)' && styles.backgroundColor !== 'transparent';
        }).catch(() => false);
        
        console.log(`🎨 Button styled: ${hasStyledButton ? '✅' : '❌'}`);
        
        // Test direct asset access
        const assetUrl = 'http://localhost/assets/frappe/dist/css/website.bundle.I7XAN4MM.css';
        console.log(`🔗 Testing asset: ${assetUrl}`);
        
        const assetResponse = await page.goto(assetUrl);
        console.log(`📄 Asset status: ${assetResponse.status()}`);
        
        if (assetResponse.status() === 200) {
            console.log('✅ CSS assets are loading correctly!');
        } else {
            console.log('❌ CSS assets still not loading');
        }
        
    } catch (error) {
        console.error('❌ Test error:', error.message);
    } finally {
        setTimeout(() => browser.close(), 3000);
    }
}

testStyling().catch(console.error);