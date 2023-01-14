npx tailwindcss -i ./icon_rhizome_dev/assets/css/main.css -o ./icon_rhizome_dev/static/css/style.css --watch
uvicorn icon_rhizome_dev.main:app --reload
