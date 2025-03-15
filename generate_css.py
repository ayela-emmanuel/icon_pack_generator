import os
import json

# Configuration
svg_folder = 'icons'       # Folder where your .svg files live
output_json = 'icons.json' # JSON metadata file
output_css = 'icons.css'   # CSS file for basic .icon styling
output_html = 'demo.html'  # Demo HTML file
items_per_page = 40        # Number of icons per page
max_page_buttons = 10      # Maximum numbered pagination buttons to show

def readable_class_name(name):
    """
    Generate a simpler 'alias' from the raw file name.
    If there are more than 3 underscore parts, keep the first two and the last part.
    Otherwise, join all parts with hyphens.
    """
    parts = name.split('_')
    if len(parts) > 3:
        selected = parts[:2] + [parts[-1]]
    else:
        selected = parts
    return '-'.join(part.lower() for part in selected)

# 1) Build a JSON array of icon data
icons_data = []
for filename in os.listdir(svg_folder):
    if filename.lower().endswith('.svg'):
        full_name, _ = os.path.splitext(filename)
        alias = readable_class_name(full_name)
        icons_data.append({
            "full_name": full_name,
            "alias": alias,
            "svgPath": f"{svg_folder}/{filename}"
        })

# Write icons.json
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(icons_data, f, indent=2)


css_content = """/* Global icon styles */
:root {
  --icon-size: 2rem;       /* default icon size */
  --icon-color: #333;      /* default icon color */
}

.icon {
  display: inline-block;
  width: var(--icon-size);
  height: var(--icon-size);
  background-color: var(--icon-color);
  /* We color the icon via background-color and mask it */
  mask-repeat: no-repeat;
  mask-position: center;
  mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  -webkit-mask-size: contain;
}
"""

with open(output_css, 'w', encoding='utf-8') as css_file:
    css_file.write(css_content)


html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>SVG Icons Demo (JSON-based Pagination)</title>
  <link rel="stylesheet" href="{output_css}">
  <style>
    body {{
      font-family: sans-serif;
      padding: 2rem;
      background: #f9f9f9;
      margin: 0;
    }}
    h1 {{
      text-align: center;
      margin-top: 0;
    }}
    .search-container {{
      text-align: center;
      margin-bottom: 1rem;
    }}
    .search-container input {{
      padding: 0.5rem;
      width: 80%;
      max-width: 300px;
      font-size: 1rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 1rem;
      margin-top: 2rem;
    }}
    .grid-item {{
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 1rem;
      text-align: center;
    }}
    .classname {{
      font-size: 0.85rem;
      color: #555;
      margin-top: 0.5rem;
      word-break: break-all;
    }}
    .pagination {{
      text-align: center;
      margin-top: 1rem;
    }}
    .pagination button {{
      padding: 0.5rem 1rem;
      margin: 0 0.25rem;
      font-size: 1rem;
      cursor: pointer;
    }}
  </style>
</head>
<body>
  <h1>SVG Icons Demo</h1>
  <div class="search-container">
    <input type="text" id="searchInput" placeholder="Search icons...">
  </div>
  <div class="grid" id="iconGrid">
    <!-- Icons will be dynamically inserted here -->
  </div>
  <div class="pagination" id="paginationControls"></div>

  <script>
    (function() {{
      'use strict';

      // Config from Python
      const itemsPerPage = {items_per_page};
      const maxPageButtons = {max_page_buttons};

      // DOM references
      const searchInput = document.getElementById('searchInput');
      const iconGrid = document.getElementById('iconGrid');
      const paginationControls = document.getElementById('paginationControls');

      // State variables
      let allIcons = [];       // Full array of icon objects
      let currentPage = 1;     // Current page in pagination

      // Simple debounce utility
      function debounce(fn, delay) {{
        let timer = null;
        return function(...args) {{
          if (timer) clearTimeout(timer);
          timer = setTimeout(() => fn.apply(this, args), delay);
        }};
      }}

      // Create HTML for one icon item
      function generateIconHTML(icon) {{
        
        return `
          <div class="grid-item" data-name="icon-${{icon.alias}}">
            <div class="icon" style="
              mask-image: url('${{icon.svgPath}}');
              -webkit-mask-image: url('${{icon.svgPath}}');
            "></div>
            <div class="classname">icon-${{icon.alias}}</div>
          </div>
        `;
      }}

      // Render the entire grid for the current page
      function renderPage(page) {{
        currentPage = page;

        const searchTerm = searchInput.value.trim().toLowerCase();
        // Filter icons based on the search (alias or full_name)
        const filtered = allIcons.filter(icon =>
          icon.alias.toLowerCase().includes(searchTerm) ||
          icon.full_name.toLowerCase().includes(searchTerm)
        );

        // Calculate total pages for the filtered set
        const totalPages = Math.ceil(filtered.length / itemsPerPage);

        // Clamp 'page' if user typed something that reduces total pages
        if (currentPage > totalPages) {{
          currentPage = Math.max(totalPages, 1);
        }}

        // Start/end indexes for the current page
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;

        // Get only the slice of icons for this page
        const pageItems = filtered.slice(start, end);

        // Build & insert HTML for the page
        iconGrid.innerHTML = pageItems.map(generateIconHTML).join('');

        // Update pagination controls
        renderPagination(totalPages);
      }}

      // Render the pagination buttons
      function renderPagination(totalPages) {{
        paginationControls.innerHTML = '';

        if (totalPages <= 1) return;

        // Helper to create a button
        function createButton(text, disabled, onClick) {{
          const btn = document.createElement('button');
          btn.textContent = text;
          btn.disabled = disabled;
          btn.addEventListener('click', onClick);
          return btn;
        }}

        // "Prev" button
        paginationControls.appendChild(
          createButton('Prev', currentPage === 1, () => renderPage(currentPage - 1))
        );

        // Numbered buttons
        let startPage = Math.max(1, currentPage - Math.floor(maxPageButtons / 2));
        let endPage = startPage + maxPageButtons - 1;
        if (endPage > totalPages) {{
          endPage = totalPages;
          startPage = Math.max(1, endPage - maxPageButtons + 1);
        }}

        for (let p = startPage; p <= endPage; p++) {{
          paginationControls.appendChild(
            createButton(p, p === currentPage, () => renderPage(p))
          );
        }}

        // "Next" button
        paginationControls.appendChild(
          createButton('Next', currentPage === totalPages, () => renderPage(currentPage + 1))
        );
      }}

      // Debounced search
      const debouncedSearch = debounce(() => {{
        renderPage(1);
      }}, 300);

      searchInput.addEventListener('input', debouncedSearch);

      // Fetch icons.json and initialize
      fetch('{output_json}')
        .then(response => response.json())
        .then(data => {{
          allIcons = data;  // store the full array of icon objects
          renderPage(1);    // render the first page
        }})
        .catch(err => {{
          iconGrid.innerHTML = '<p style="color:red">Error loading icon data: ' + err + '</p>';
        }});
    }})();
  </script>
</body>
</html>
"""

# Write out the HTML demo
with open(output_html, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print(f"JSON file generated: {output_json}")
print(f"CSS file generated: {output_css}")
print(f"Demo HTML generated: {output_html}")
print("Done! Open demo.html in your browser to test JSON-based pagination/search.")
