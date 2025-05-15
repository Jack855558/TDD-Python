from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

# HTML template with interactive graph via vis.js
TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>arXiv Citation Graph</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: auto; padding: 2em; }
    #network { width: 100%; height: 600px; border: 1px solid #ccc; margin-top: 1em; }
  </style>
</head>
<body>
  <h1>arXiv Citation Graph</h1>
  <form id="id-form">
    <label for="arxiv_id">Enter arXiv ID:</label><br>
    <input type="text" id="arxiv_id" name="arxiv_id" placeholder="e.g., 2101.00001" required style="width:70%;padding:0.5em;">
    <button type="submit" style="padding:0.5em 1em;">Build Graph</button>
  </form>
  <div id="network"></div>
  <script>
    const form = document.getElementById('id-form');
    let network = null;
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const id = document.getElementById('arxiv_id').value.trim();
      if (!id) return;
      const resp = await fetch('/graph/' + encodeURIComponent(id));
      const data = await resp.json();

      const nodes = new vis.DataSet(data.nodes);
      const edges = new vis.DataSet(data.edges);
      const container = document.getElementById('network');
      const graphData = { nodes, edges };
      const options = {
        physics: { stabilization: true },
        nodes: { shape: 'dot', size: 16, font: { size: 14 } },
        edges: { arrows: { to: { enabled: true, scaleFactor: 0.5 } } }
      };

      if (network) {
        network.destroy();
      }
      network = new vis.Network(container, graphData, options);
    });
  </script>
</body>
</html>
'''

# Semantic Scholar API endpoint: include paperId and title
SEMANTIC_SCHOLAR_URL = (
    'https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}?' 
    'fields=references.paperId,references.title'
)

@app.route('/', methods=['GET'])
def index():
    return render_template_string(TEMPLATE)

@app.route('/graph/<arxiv_id>')
def graph(arxiv_id):
    nodes = []
    edges = []
    seen = set()

    def fetch_refs(paper_id, label, depth):
        if depth > 1 or paper_id in seen:
            return
        seen.add(paper_id)
        nodes.append({'id': paper_id, 'label': label})

        url = SEMANTIC_SCHOLAR_URL.format(id=paper_id)
        r = requests.get(url)
        if r.status_code != 200:
            return
        data = r.json()
        refs = data.get('references') or []
        for ref in refs:
            child_id = ref.get('paperId')
            child_title = ref.get('title') or ref.get('paperId')
            if not child_id:
                continue
            edges.append({'from': paper_id, 'to': child_id})
            fetch_refs(child_id, child_title, depth + 1)

    # First, fetch the original to get title
    # We use Semantic Scholar lookup by arXiv to get title
    meta = requests.get(
        f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=title"
    )
    if meta.status_code == 200:
        title = meta.json().get('title', arxiv_id)
    else:
        title = arxiv_id

    fetch_refs(arxiv_id, title, 0)

    # Dedupe nodes
    unique = {node['id']: node for node in nodes}
    return jsonify({'nodes': list(unique.values()), 'edges': edges})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
