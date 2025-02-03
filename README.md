# 📌 ASD MRI Classification - README

## 🔹 Overview
This project is a web-based system for classifying autism from MRI scans using **Inception v3** with **Transfer Learning**. The system leverages a pretrained **Inception v3** model, fine-tuned specifically for ASD classification, to improve accuracy and efficiency. 

The system consists of:
- **Frontend:** React.js for the UI.
- **Backend:** Python (Flask) for handling image uploads and classification.
- **Deep Learning Model:** Pretrained **Inception v3** model fine-tuned for ASD classification using Transfer Learning.

---

## 🔧 Installation

### 🖥️ 1. Clone the Repository
```sh
git clone https://github.com/NitzanEz/Final-Project.git
```

---

## 🛠 Backend (Python & Flask)

### 📦 2. Set Up a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 📥 3. Install Required Python Libraries
```sh
pip install -r backend/requirements.txt
```

#### 📄 **`backend/requirements.txt`** (included in repo)
```
Flask
Flask-CORS
numpy
pandas
torch
torchvision
Pillow
nibabel
tensorflow
```

### 🔹 4. Download Model Weights
The trained model weights must be downloaded and placed in the backend directory:
- **Download the weights from:** https://drive.google.com/file/d/1JAEwojy8jmsvn9k8iX9ZqEHWXE4YXbm8/view?usp=drive_link
- **Save them to:** `Final-Project/GUI/backend/`

### ▶️ 5. Run the Backend
```sh
cd backend
python app.py
```
- The backend should start running on **http://127.0.0.1:5000**.

---

## 🌐 Frontend (React.js)

### 📥 6. Install Node.js & npm (if not installed)
- Download & install Node.js from [here](https://nodejs.org/).
- Verify installation:
```sh
node -v
npm -v
```

### 📦 7. Install React Dependencies
```sh
cd frontend
npm install
```

#### 📄 **`frontend/package.json` (Main Dependencies)**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.1",
    "axios": "^1.5.0",
    "bootstrap": "^5.3.0",
    "@mui/material": "^5.15.0"
  }
}
```

### ▶️ 8. Run the Frontend
```sh
npm start
```
- React app should open automatically at **http://localhost:3000**.

---

## 🛠 Usage
1. **Login as a doctor** using the credentials stored in `users.json`.
2. **Search for a patient** by ID.
3. **Upload a `.nii` MRI file**.
4. Click **Classify** → The deep learning model will analyze the scan.
5. Results are stored in the **patient's history JSON file**.

---

## 📌 API Endpoints (Flask Backend)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload an `.nii` MRI file |
| `POST` | `/classify` | Run ASD classification on the MRI |
| `GET` | `/patients/<id>` | Fetch patient details |
| `POST` | `/login` | Doctor login authentication |

---

## 🛠 Deployment
For production, use:
```sh
npm run build   # Build frontend for production
python app.py   # Start backend in production mode
```
You can deploy using **Docker**, **AWS**, or **Heroku**.

---

## 📌 Troubleshooting
### 🔹 Backend Issues
- If Flask doesn't start, check port conflicts: `lsof -i :5000`
- Verify the model `.pth` file exists and is loaded properly.

### 🔹 Frontend Issues
- Run `npm audit fix` if package vulnerabilities appear.
- If styles break, try `npm install bootstrap`.

---

## 📌 Authors
- **Your Name** - *Lead Developer*
- **Contributors** - *Other Team Members*

---

## 📌 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

🚀 **Happy Coding! Let me know if you need modifications!**

