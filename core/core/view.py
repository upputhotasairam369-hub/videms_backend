# pyrefly: ignore [missing-import]
from django.http import HttpResponse

def home_view(request):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Videms Backend API</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #FAFAFA;
            --text-primary: #111827;
            --text-secondary: #6B7280;
            --accent: #2563EB;
            --border: #E5E7EB;
            --card-bg: #FFFFFF;
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: var(--font-family);
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
        }
        header {
            padding: 80px 0 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border);
            margin-bottom: 40px;
        }
        .header-content {
            max-width: 600px;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            background-color: #EFF6FF;
            color: var(--accent);
            font-size: 12px;
            font-weight: 600;
            border-radius: 9999px;
            margin-bottom: 16px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        h1 {
            font-size: 42px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 16px;
            color: var(--text-primary);
        }
        .description {
            font-size: 18px;
            color: var(--text-secondary);
            font-weight: 400;
            line-height: 1.6;
        }
        .illustration {
            width: 320px;
            height: 240px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .shape-1 {
            position: absolute;
            width: 180px;
            height: 180px;
            border: 2px solid var(--border);
            border-radius: 50%;
            top: 20px;
            left: 20px;
        }
        .shape-2 {
            position: absolute;
            width: 140px;
            height: 140px;
            background-color: #EFF6FF;
            border-radius: 12px;
            top: 60px;
            right: 40px;
            transform: rotate(15deg);
        }
        .shape-3 {
            position: absolute;
            width: 80px;
            height: 80px;
            background-color: var(--accent);
            border-radius: 8px;
            bottom: 40px;
            left: 100px;
        }
        
        main {
            padding-bottom: 80px;
        }
        .section-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 24px;
        }
        
        .endpoints-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .endpoint-row {
            display: flex;
            align-items: center;
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            height: 70px;
            padding: 0 20px;
            text-decoration: none;
            transition: all 150ms ease;
            color: inherit;
        }
        
        .endpoint-row:hover {
            border-color: var(--accent);
        }
        
        .endpoint-row:focus-visible {
            outline: 2px solid var(--accent);
            outline-offset: 2px;
        }
        
        .icon {
            color: var(--text-secondary);
            width: 20px;
            height: 20px;
            margin-right: 16px;
            flex-shrink: 0;
            transition: color 150ms ease;
        }
        
        .endpoint-row:hover .icon {
            color: var(--accent);
        }
        
        .endpoint-name {
            font-weight: 600;
            font-size: 15px;
            width: 200px;
            flex-shrink: 0;
        }
        
        .endpoint-desc {
            color: var(--text-secondary);
            font-size: 14px;
            flex-grow: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            padding-right: 20px;
        }
        
        .btn-open {
            font-size: 13px;
            font-weight: 500;
            color: var(--accent);
            background-color: #EFF6FF;
            padding: 6px 12px;
            border-radius: 6px;
            opacity: 0;
            transition: opacity 150ms ease;
        }
        
        .endpoint-row:hover .btn-open {
            opacity: 1;
        }
        
        footer {
            border-top: 1px solid var(--border);
            padding: 40px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-secondary);
            font-size: 13px;
        }
        
        .tech-stack span {
            font-weight: 500;
            color: var(--text-primary);
        }
        
        @media (max-width: 768px) {
            header {
                flex-direction: column;
                align-items: flex-start;
                padding: 60px 0 40px;
            }
            .illustration {
                display: none;
            }
            h1 {
                font-size: 32px;
            }
            .endpoint-row {
                height: auto;
                padding: 16px;
                flex-wrap: wrap;
            }
            .endpoint-name {
                width: 100%;
                margin-bottom: 4px;
            }
            .endpoint-desc {
                width: 100%;
                padding-right: 0;
                margin-bottom: 12px;
                white-space: normal;
            }
            .btn-open {
                opacity: 1;
                margin-left: 36px;
            }
            footer {
                flex-direction: column;
                gap: 16px;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-content">
                <span class="badge">VIDEMS</span>
                <h1>Videms Backend API</h1>
                <p class="description">Manage and explore all backend services powering the Videms eCommerce application.</p>
            </div>
            <div class="illustration" aria-hidden="true">
                <div class="shape-1"></div>
                <div class="shape-2"></div>
                <div class="shape-3"></div>
            </div>
        </header>

        <main>
            <h2 class="section-title">Available Endpoints</h2>
            <div class="endpoints-list">
                
                <a href="/admin/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <div class="endpoint-name">Admin Panel</div>
                    <div class="endpoint-desc">Django administration interface for managing records</div>
                    <div class="btn-open">Open</div>
                </a>

                <a href="/api/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                    </svg>
                    <div class="endpoint-name">API Root</div>
                    <div class="endpoint-desc">Browse all registered API endpoints</div>
                    <div class="btn-open">Open</div>
                </a>

                <a href="/api/products/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                    <div class="endpoint-name">Products</div>
                    <div class="endpoint-desc">Retrieve and filter product listings</div>
                    <div class="btn-open">Open</div>
                </a>

                <a href="/api/categories/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                    <div class="endpoint-name">Categories</div>
                    <div class="endpoint-desc">Browse product categories and metadata</div>
                    <div class="btn-open">Open</div>
                </a>

                <a href="/api/banners/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <div class="endpoint-name">Banners</div>
                    <div class="endpoint-desc">Manage hero carousel marketing banners</div>
                    <div class="btn-open">Open</div>
                </a>

                <a href="/api/combinations/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    <div class="endpoint-name">Shop by Combination</div>
                    <div class="endpoint-desc">Collections of products forming complete setups</div>
                    <div class="btn-open">Open</div>
                </a>

                <a href="/api/home/bestsellers/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                    <div class="endpoint-name">Our Bestsellers</div>
                    <div class="endpoint-desc">Top-performing products curated for the homepage</div>
                    <div class="btn-open">Open</div>
                </a>

                <a href="/api/home/new-arrivals/" class="endpoint-row">
                    <svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                    <div class="endpoint-name">New Arrivals</div>
                    <div class="endpoint-desc">The latest furniture pieces added to the store</div>
                    <div class="btn-open">Open</div>
                </a>
            </div>
        </main>

        <footer>
            <div class="tech-stack">
                Built with <span>Django</span>, <span>Django REST Framework</span>, and <span>PostgreSQL</span>
            </div>
            <div class="version">
                v1.0
            </div>
        </footer>
    </div>
</body>
</html>
"""
    return HttpResponse(html_content)