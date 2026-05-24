"""Simple script to capture Flow API endpoints."""

import asyncio
import json
from playwright.async_api import async_playwright


async def capture_flow_api():
    """Capture Flow API requests."""
    captured_requests = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Listen for all requests
        async def handle_request(request):
            url = request.url
            # Filter for Flow API requests
            if any(x in url for x in ['labs.google', '/api/', 'flow']):
                headers = await request.all_headers()
                captured_requests.append({
                    'method': request.method,
                    'url': url,
                    'headers': headers,
                    'post_data': request.post_data
                })
                print(f"Captured: {request.method} {url[:100]}")

        # Listen for responses
        async def handle_response(response):
            request = response.request
            url = request.url

            if any(x in url for x in ['labs.google', '/api/', 'flow']):
                try:
                    body = await response.text()
                    print(f"Response {response.status}: {url[:80]}")

                    # Store the full request/response
                    captured_requests.append({
                        'type': 'response',
                        'method': request.method,
                        'url': url,
                        'status': response.status,
                        'response_body': body[:500],  # First 500 chars
                    })
                except:
                    pass

        page = await context.new_page()
        page.on('request', handle_request)
        page.on('response', handle_response)

        print("Navigating to Flow...")
        await page.goto('https://labs.google/fx/tools/flow')

        print("\nWaiting 60 seconds for you to interact with Flow...")
        print("Try to:")
        print("1. Log in if needed")
        print("2. Generate an image")
        print("3. Check the results")
        print("\nPress Ctrl+C to stop early\n")

        try:
            await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("\nStopping...")

        await browser.close()

        # Save captured requests
        with open('flow_api_captured.json', 'w') as f:
            json.dump(captured_requests, f, indent=2)

        print(f"\n✓ Saved {len(captured_requests)} requests to flow_api_captured.json")

        # Print summary
        print("\n=== API Endpoints Discovered ===")
        unique_endpoints = set()
        for req in captured_requests:
            if 'url' in req:
                # Extract path from URL
                from urllib.parse import urlparse
                parsed = urlparse(req['url'])
                endpoint = f"{req.get('method', 'GET')} {parsed.path}"
                unique_endpoints.add(endpoint)

        for endpoint in sorted(unique_endpoints):
            print(endpoint)


if __name__ == '__main__':
    asyncio.run(capture_flow_api())
