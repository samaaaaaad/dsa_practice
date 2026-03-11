# The following script automates my process of moving my solutions from my local machine to Github and at the same time updates the tracker in the README

import os
import shutil
from datetime import datetime

# --- CONFIG ---
DOWNLOADS_PATH = os.path.expanduser("~/Downloads") 
REPO_PATH = os.getcwd() 
README_FILE = "README.md"

def update_readme(category, problem_name, filename):
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Clean up problem name for display
    display_name = problem_name.replace("-", " ").title()
    relative_path = f"./{category}/{filename}"
    
    # New row for the Markdown table
    new_row = f"| {date_str} | {display_name} | - | [Code]({relative_path}) | - |\n"
    
    if os.path.exists(README_FILE):
        with open(README_FILE, "r") as f:
            lines = f.readlines()
        
        # Find the category section in your README
        with open(README_FILE, "w") as f:
            found_section = False
            for line in lines:
                f.write(line)
                # Look for the header (e.g., ### 🟢 Arrays)
                if category.lower() in line.lower() and "###" in line:
                    found_section = True
                # Add the row after the table header separator | :--- |
                if found_section and "| :--- |" in line:
                    f.write(new_row)
                    found_section = False
        print("📝 Updated README.md table.")

def run_workflow():
    # 1. Grab the latest file
    files = [os.path.join(DOWNLOADS_PATH, f) for f in os.listdir(DOWNLOADS_PATH) 
             if os.path.isfile(os.path.join(DOWNLOADS_PATH, f))]
    
    if not files:
        print("❌ No files in Downloads.")
        return

    latest_file = max(files, key=os.path.getctime)
    extension = os.path.splitext(latest_file)[1]
    
    # 2. Getting Information
    print(f"📦 Processing: {os.path.basename(latest_file)}")
    category = input("Category (arrays/trees/dp): ").strip().lower()
    problem = input("Problem Name (e.g. Two Sum): ").strip().replace(" ", "-").lower()
    
    # 3. Moving and Renaming
    target_dir = os.path.join(REPO_PATH, category)
    os.makedirs(target_dir, exist_ok=True)
    
    new_filename = f"{problem}{extension}"
    dest_path = os.path.join(target_dir, new_filename)
    shutil.move(latest_file, dest_path)
    print(f"✅ Moved to {category}/{new_filename}")

    # 4. Updating README
    update_readme(category, problem, new_filename)

    # 5. Pushing to GitHub
    confirm = input("Push to GitHub? (y/n): ").lower()
    if confirm == 'y':
        os.system("git add .")
        os.system(f'git commit -m "Solved: {problem}"')
        os.system("git push")
        print("🚀 Live on GitHub!")

if __name__ == "__main__":
    run_workflow()
