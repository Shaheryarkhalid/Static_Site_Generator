# 🏗️ Static Site Generator  

A simple, efficient **Static Site Generator** built from scratch! 🚀  

👉 **[Live Demo](https://shaheryarkhalid.github.io/Static_Site_Generator/)**  

## 📌 Features  
✔️ Converts Markdown (`.md`) to HTML  
✔️ Supports templates for consistent layouts  
✔️ Fast, lightweight, and easy to use  
✔️ Generates fully static websites  

## 🚀 Getting Started  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Shaheryarkhalid/static_site_generator.git  
cd static_site_generator
```

### 3️⃣ Run the Generator  
```bash
main.sh
```

### 4️⃣ View the Output  
Open `docs/index.html` in your browser. 🎉  

## 🛠️ How It Works  
1. Reads content from `.md` files  
2. Applies a template to generate HTML  
3. Saves output in the `docs/` folder  

## 📂 Project Structure  
```
📦 static_site_generator  
 ┣ 📂 content       # Markdown files (your site content)  
 ┣ 📂 templates     # HTML templates for consistent design  
 ┣ 📂 docs          # Generated static site  
 ┣ 📜 main.sh       # Main script to generate the site locally
 ┣ 📜 build.sh      # Buil script to build the site for github  
 ┗ 📜 README.md     # This file  
```

## ✨ Example Usage  
```bash
./main.sh
./build.sh
```
This will generate an HTML page from `blog.md` and save it in `docs/`.
Keep in mind to update execute permission for main.sh and build.sh

```bash
sudo chmod +x './main.sh'
sudo chmod +x './build.sh'
```

## 📢 Contributing  
Feel free to **fork**, create issues, or submit PRs. Let's make it better together!  

## 📜 License  
MIT License. Free to use and modify.  

🔗 **GitHub Repo:** [Shaheryarkhalid/static_site_generator](https://github.com/Shaheryarkhalid/static_site_generator)  
