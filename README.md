<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure API Key Management</title>
    <style>
        body { font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { border-bottom: 2px solid #eee; padding-bottom: 10px; }
        h2 { color: #333; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 25px; }
        h3 { color: #555; margin-top: 20px; }
        code { background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-size: 0.9em; }
        pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        ul { list-style: disc; margin-left: 20px; }
        .warning { border: 1px solid #ffcc00; background-color: #fffacd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>

    <h1>&#x1F510; Secure API Key Management in Projects</h1>

    <p>This guide demonstrates <strong>how to safely use API keys</strong> in your Python, Node.js, or other projects <strong>without exposing them publicly</strong> on GitHub.</p>

    <hr>

    <h2 id="why-you-should-never-upload-api-keys">&#x1F6AB; Why You Should Never Upload API Keys</h2>

    <p>API keys are <strong>confidential credentials</strong> that identify your account to external services (like OpenAI, Google Cloud, AWS, etc.).<br>
    Uploading them publicly can lead to:</p>

    <ul>
        <li>&#x1F4B8; Unauthorized usage and billing</li>
        <li>&#x1F6B3; Account suspension or permanent ban</li>
        <li>&#x1F513; Data theft and security breaches</li>
    </ul>

    <p>Even if deleted later, <strong>Git history retains old commits</strong>, and bots constantly scan GitHub for leaked keys.</p>

    <hr>

    <h2 id="safe-way-use-environment-variables">&#x2705; Safe Way: Use Environment Variables</h2>

    <p>Instead of hardcoding your API keys (e.g. <code>API_KEY = "abcdef123456"</code>), you should:</p>
    <ol>
        <li>Store them in a <strong><code>.env</code> file</strong> (local only)</li>
        <li>Load them securely in your code</li>
        <li>Add <code>.env</code> to <strong><code>.gitignore</code></strong> so it’s never uploaded</li>
    </ol>

    <hr>

    <h2 id="example-python">&#x1F9E0; Example (Python)</h2>

    <h3>1. Install <code>python-dotenv</code></h3>
    <pre><code>pip install python-dotenv</code></pre>

    <h3>2. Create a <code>.env</code> file</h3>
    <pre><code>OPENWEATHER_API_KEY=your_openweather_key_here
NEWSAPI_KEY=your_newsapi_key_here</code></pre>

    <h3>3. Load keys in your code</h3>
    <pre><code>from dotenv import load_dotenv
import os

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")</code></pre>

    <h3>4. Add <code>.env</code> to <code>.gitignore</code></h3>
    <pre><code># .gitignore
.env</code></pre>

    <hr>

    <h2 id="example-nodejs">&#x1F9E0; Example (Node.js)</h2>

    <h3>1. Install <code>dotenv</code></h3>
    <pre><code>npm install dotenv</code></pre>

    <h3>2. Create <code>.env</code> file</h3>
    <pre><code>OPENAI_API_KEY=your_openai_key_here</code></pre>

    <h3>3. Load keys in your app</h3>
    <pre><code>require('dotenv').config();

const apiKey = process.env.OPENAI_API_KEY;</code></pre>

    <hr>

    <h2 id="folder-structure-example">&#x1F9EB; Folder Structure Example</h2>

    <pre><code>project/
&#9475;
&#9499;&#9472;&#9472; app.py
&#9499;&#9472;&#9472; .env
&#9499;&#9472;&#9472; .gitignore
&#9499;&#9472;&#9472; README.md</code></pre>

    <hr>

    <h2 id="extra-security-tips">&#x1F6A7; Extra Security Tips</h2>

    <ul>
        <li>Rotate (regenerate) your API keys regularly.</li>
        <li>Use separate keys for <strong>development</strong> and <strong>production</strong>.</li>
        <li>Never share screenshots or logs showing your keys.</li>
        <li>If you accidentally commit a key, <strong>revoke it immediately</strong> from the provider’s dashboard.</li>
    </ul>

    <hr>

    <h2 id="useful-references">&#x1F4DA; Useful References</h2>

    <ul>
        <li><a href="https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository">GitHub Docs: Removing sensitive data</a></li>
        <li><a href="https://blog.postman.com/how-to-securely-use-api-keys/">12 Best Practices for API Key Security (Postman Blog)</a></li>
        <li><a href="https://github.com/motdotla/dotenv">dotenv GitHub Repository</a></li>
    </ul>

    <hr>

    <p><strong>Remember:</strong></p>

    <blockquote>
        <em>Treat your API keys like passwords — never expose them publicly.</em>
    </blockquote>

    <hr>

    <p><strong>Author:</strong> [Your Name]<br>
    <strong>License:</strong> MIT</p>

</body>
</html>
