from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# HTML template with citations section
TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>arXiv Citation Fetcher</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 2em; }
      input[type=text] { width: 70%; padding: 0.5em; }
      button { padding: 0.5em 1em; }
      ul { margin-top: 1em; }
      .section { margin-top: 2em; }
    </style>
  </head>
  <body>
    <h1>arXiv Citation Fetcher</h1>
    <form method="post">
      <label for="arxiv_id">Enter arXiv ID:</label><br>
      <input type="text" id="arxiv_id" name="arxiv_id" placeholder="e.g., 2101.00001" required>
      <button type="submit">Fetch Citations</button>
    </form>

    {% if citations %}
      <div class="section">
        <h2>Cited Papers in {{ arxiv_id }}</h2>
        <ul>
        {% for c in citations %}
          <li>
            {% if c['url'] %}
              <a href="{{ c['url'] }}" target="_blank">{{ c['title'] }}</a>
            {% else %}
              {{ c['title'] }}
            {% endif %}
            {% if c['year'] %} ({{ c['year'] }}){% endif %}
          </li>
        {% endfor %}
        </ul>
      </div>
    {% endif %}

    {% if error %}
      <div class="section">
        <p style="color: red;">{{ error }}</p>
      </div>
    {% endif %}
  </body>
</html>
'''

# Semantic Scholar API endpoint for references
SEMANTIC_SCHOLAR_URL = (
    'https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}?' 
    'fields=references.title,references.externalIds,references.year'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    citations = []
    error = None
    arxiv_id = None
    if request.method == 'POST':
        arxiv_id = request.form['arxiv_id'].strip()
        url = SEMANTIC_SCHOLAR_URL.format(id=arxiv_id)
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            refs = data.get('references') or []
            if not refs:
                error = 'No references found or citations data unavailable.'
            else:
                for r in refs:
                    ext = r.get('externalIds') or {}
                    link = None
                    # Safely check in ext
                    if isinstance(ext, dict) and ext.get('ArXiv'):
                        link = f"https://arxiv.org/abs/{ext['ArXiv']}"
                    elif isinstance(ext, dict) and ext.get('DOI'):
                        link = f"https://doi.org/{ext['DOI']}"
                    citations.append({
                        'title': r.get('title', 'No title'),
                        'year': r.get('year'),
                        'url': link
                    })
        else:
            error = f'Error fetching data (status code {resp.status_code}).'
    return render_template_string(TEMPLATE, citations=citations, arxiv_id=arxiv_id, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
