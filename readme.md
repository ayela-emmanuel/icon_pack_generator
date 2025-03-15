[View Demo](https://ayela-emmanuel.github.io/icon_pack_generator/demo.html).

1. **How to Host** the generated files locally or on a simple web server.  
2. **How to Use** (both self-contained usage and usage of the Python script).  
3. Any other relevant notes about `generate_css.py`.

Feel free to adjust wording, file names, or structure as needed.

---

# README

## Overview

This project contains a Python script (`generate_css.py`) that automates the creation of:

1. A **CSS** file (`icons.css`) defining a global `.icon` style.  
2. A **JSON** file (`icons.json`) containing metadata for all your `.svg` icons.  
3. A **demo HTML** file (`demo.html`) that:
   - Dynamically loads icon data from `icons.json`.
   - Displays icons in a grid.
   - Implements a search field.
   - Provides pagination controls.

This approach keeps the HTML lean even if you have thousands of icons.

---

## Getting Started

### 1. Folder Structure

Make sure your environment has a folder structure similar to:

```
.
├── icons/
│   ├── icon1.svg
│   ├── icon2.svg
│   └── ...
├── generate_css.py
├── README.md
```

All your `.svg` icons should be in the `icons/` subfolder. The Python script will scan that folder.

### 2. Run `generate_css.py`

You can run the script directly in your terminal or command prompt:

```bash
python generate_css.py
```

It will generate:

- **`icons.json`** – A JSON file describing each icon (`alias`, full name, file path).  
- **`icons.css`** – A CSS file containing the `.icon` styling.  
- **`demo.html`** – The single-page application that shows a grid of icons and includes search + pagination.

### 3. Confirm Output

After running the script, you should see three new files in your folder:

- `icons.json`
- `icons.css`
- `demo.html`

Open `demo.html` in your browser to confirm everything worked.

---

## How to Host

Once you have the generated files, you can host them locally or upload them to a simple web server:

### Local Hosting (Python’s Built-in Server)

From the folder containing `demo.html`, run:

```bash
python -m http.server 8000
```

Then open your browser to [http://localhost:8000/demo.html](http://localhost:8000/demo.html).

### Hosting on a Static Server

You can place these files on **any** static web host (e.g., GitHub Pages, Netlify, Amazon S3, etc.). Just ensure that:

1. `demo.html` is accessible at some URL.  
2. `icons.json` and `icons.css` are in the same relative paths as generated (or you update the paths in `demo.html` if you change the structure).  
3. The `icons/` folder of SVGs is also served at the correct relative path, so the mask images load correctly.

---

## How to Use (Self-Contained)

If you want a **self-contained** version for simpler offline usage:

1. Make sure you keep the file structure as generated:
   ```
   .
   ├── demo.html
   ├── icons.css
   ├── icons.json
   ├── icons/
   │   ├── ...
   ```
2. Just **open** `demo.html` directly in your browser (e.g., double-click).  
   - Some browsers block `fetch()` requests to local files for security reasons. In that case, you **must** use a local server (see **Local Hosting** above).

---

## How to Use `generate_css.py` in Detail

1. **Prerequisites**: You need Python 3 installed.  
2. **Usage**:
   1. Put all `.svg` icon files inside `icons/`.  
   2. Open a terminal in the same directory as `generate_css.py`.  
   3. Run:  
      ```bash
      python generate_css.py
      ```  
   4. The script scans `icons/` for `.svg` files and creates:
      - `icons.json` with metadata (full name, alias, and path).
      - `icons.css` containing a global `.icon` style.
      - `demo.html` with search + pagination logic that fetches data from `icons.json`.
3. **Customization**:  
   - You can edit the **configuration variables** at the top of `generate_css.py`, such as:
     - `svg_folder = "icons"`
     - `output_css = "icons.css"`
     - `output_html = "demo.html"`
     - `items_per_page = 40` (or any other number)
     - `max_page_buttons = 10`  

---

## Troubleshooting

- **Icons not loading**: Ensure your `icons/` path is correct and that each `.svg` file has the proper name (e.g., `icon-star.svg`).
- **Search not working**: Confirm you opened `demo.html` via a local server rather than a direct file path. Some browsers block `fetch()` calls on local file URIs.
- **Pagination issues**: If you have thousands of icons, confirm you adjusted `items_per_page` as needed. Large sets can still be handled, but you may want more advanced lazy-loading if performance becomes an issue.

---

**Enjoy your icon set!**  
Feel free to modify `generate_css.py` or `demo.html` to meet your specific use case. If you run into any issues, open an [Issue](#).