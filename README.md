# 🔒 Encrypter-Decrypter 🔓  
**"Secure Your Files and Hide Your Secrets – Powered by Django!"**

Welcome to **Encrypter-Decrypter**, your ultimate tool for protecting sensitive data and secrets! This project combines the power of encryption, decryption, and **LSB Steganography** to make your data not only secure but also untraceable. With a backend powered by **Django**, this project ensures efficiency, reliability, and scalability.  

## 🌟 Features

1. **File Encryption & Decryption**  
   - Encrypt any file for secure storage or sharing.  
   - Decrypt your files safely to regain access.  

2. **Message Hiding with LSB Steganography**  
   - Seamlessly embed secret messages into images using **Least Significant Bit (LSB)** steganography.  
   - Effortlessly extract hidden messages from image files.  

3. **Powered by Django**  
   - A robust backend built using Django ensures a structured and scalable application.

4. **User-Friendly Interface**  
   - Beautiful design crafted with **HTML**, **CSS**, and **SCSS**.  

5. **Cross-Language Support**  
   - Core functionalities powered by **Python** with interactive **JavaScript** for the front end.  

## 📋 Limitations

- LSB Steganography works best with uncompressed formats like `.bmp` or `.png`. Using compressed formats such as `.jpg` may lead to hidden data loss.  
- Encryption and decryption of large files may take longer depending on the file size and system resources.

## 🚀 Getting Started  

Follow these steps to set up the project locally.

### Prerequisites

- **Python** (>= 3.8)  
- **Poetry** (Dependency Manager)  
- **Django**  

To install **Poetry**, run:  
```bash
pip install poetry
```

### Installation

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/suchitgudulkar/Encrypter-decrypter.git && cd Encrypter-decrypter
   ```

2. **Install the `poetry` for Installing & Managing dependacies**:
   Downloads and installs the `poetry` for installing and managing different project's dependacies locally!
   ```bash
    pip3 install poetry
   ```

3. **Install the Dependencies:**  
   Using **Poetry**, install the required dependencies:  
   ```bash
   poetry install --noroot
   ```

4. **Run Django Migrations:**  
   Set up the database for the Django application:  
   ```bash
   poetry run python manage.py migrate
   ```

5. **Start the Development Server:**  
   ```bash
   poetry run python3 manage.py runserver
   ```

## 🛠️ Technology Stack  

- **Framework:** Django  
- **Front-end:** HTML, CSS, SCSS, JavaScript  
- **Back-end:** Python  
- **Dependency Management:** Poetry  
- **Image Processing:** LSB Steganography  

## 🖼️ How it Works? 

### 1. File Encryption & Decryption  
   Encrypt files securely so you can share or store them without worrying about unauthorized access.  

### 2. Message Hiding with LSB Steganography  
   - Hide secret text messages into image files.  
   - Retrieve those hidden messages effortlessly.  

## 🤝 Contributing  

Contributions are always welcome!  
Feel free to fork the repository and submit pull requests.  

## 📜 License  

This project is licensed under the [MIT License](LICENSE).  

## 🎉 Acknowledgements  

Special thanks to the open-source community for the tools and libraries that made this project possible.
