# RAG Hands-On

## Prerequisites
To run this project, ensure you have the following installed:

- **Python**: Version >= `3.10.0`
- **Required Libraries**:

```bash
haystack-ai==2.2.4
mongodb-atlas-haystack==0.3.0
ollama-haystack==0.0.6
sentence-transformers==3.1.1
streamlit==1.34.0
```

### Installation Instructions
To install all required dependencies, execute the following command:

```bash
pip install -r requirements.txt
```

## Configuring the Code

1. **Update the MongoDB Connection**
   - Open `osaka_tourism_chatbot.py` in a text editor.
   - Locate the `"MONGO_CONNECTION"` variable.
   - Replace its value with your MongoDB Connection String (provided in the PPT).

2. **Set the Server IP Address**
   - Find the `"IP_ADDRESS"` variable.
   - Replace it with your server’s actual IP address.
   - Ensure you have deployed **Llama 3.2** using **OLLAMA** before proceeding.

## Running the Program
To start the chatbot, execute the following command:

```bash
python -m streamlit run osaka_tourism_chatbot.py
```

## Accessing the Web Interface
Once the program is running, open your web browser and visit:

```
http://your_server_ip_address:8501/
```

Replace `your_server_ip_address` with the actual IP of your server.

## Troubleshooting
- Ensure Python and all dependencies are correctly installed.
- Verify that **OLLAMA** is running and properly set up with Llama 3.2.
- Double-check the MongoDB connection string for any typos or incorrect credentials.
- If the app does not load, ensure that **port 8501** is open in your firewall settings.

---

This guide should help you successfully set up and run the **Osaka Tourism Chatbot** using Retrieval-Augmented Generation (RAG). Happy coding!