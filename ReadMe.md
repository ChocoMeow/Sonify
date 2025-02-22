# Sonify

<img align="right" src="https://github.com/user-attachments/assets/db05b4a7-a182-47f2-9a16-b762a1cc77bd" width=130 alt="Lavalink logo">

Sonify is an AI-powered music generator that allows users to create music by providing lyrics or selecting a style of music. The project leverages cutting-edge AI models for generating music, lyrics, and even custom thumbnails for each song. The system is inspired by projects like Suno and Riffusion.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

Sonify allows users to input lyrics or select a desired musical style, and in return, it generates a complete song. The system integrates several AI technologies:

- **[YuE](https://github.com/multimodal-art-projection/YuE)** for generating the music
- **ChatGPT** for generating lyrics
- **[Stable Diffusion](https://github.com/CompVis/stable-diffusion)** for generating an eye-catching song thumbnail

This integration provides a seamless experience where musical creativity is just a few inputs away.

## Tech Stack

- **Frontend:** [Vite + Vue.js](https://github.com/multimodal-art-projection/YuE)
- **Backend:** [Flask (Python)](https://flask.palletsprojects.com/en/stable/)

## Architecture

The project is structured as a single repository with both frontend and backend components:

- **Frontend:**  
  The user interface built with Vue.js using Vite for fast development and optimized builds. It serves as the primary interaction platform where users can enter lyrics or pick a style.

- **Backend:**  
  A Python Flask API that handles the core functionalities:
  - Music generation using the YuE model.
  - Lyrics generation with ChatGPT.
  - Thumbnail generation with Stable Diffusion.

The components communicate seamlessly to deliver a smooth end-to-end experience.

## Features

- **AI Music Generation:**  
  Generate custom music tracks based on user inputs.

- **Custom Lyrics Generation:**  
  Use ChatGPT to create lyrics or complement user-provided lyrics.

- **Thumbnail Generation:**  
  Automatically generate attractive thumbnails for your song using Stable Diffusion.

- **User Inputs:**  
  Support for both lyric-based and style-based music generation.

- **Modern UI:**  
  A sleek and user-friendly interface built with Vue.js for a smooth interaction experience.

## Setup and Installation

### Prerequisites

- **Node.js 22 or later** and **npm/yarn** (for the frontend)
- **Python 3.8+** (for the backend)
- Ensure you have the necessary libraries and environment setups for AI model integrations (check documentation from YuE, ChatGPT API, and Stable Diffusion).

### Clone the Repository

```bash
git clone https://github.com/ChocoMeow/sonify.git
cd sonify
```

### Frontend Setup

1. Navigate to the frontend directory.
2. Install dependencies:

   ```bash
   npm install
   # or
   yarn install
   ```

3. Run the development server:

   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Backend Setup

1. Navigate to the backend directory.
2. Create a virtual environment and activate it (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set any necessary environment variables (e.g., API keys for ChatGPT, Stable Diffusion, etc.):

   ```bash
   export CHATGPT_API_KEY=your_chatgpt_api_key
   export STABLE_DIFFUSION_API_KEY=your_stable_diffusion_api_key
   # etc.
   ```

5. Run the Flask application:

   ```bash
   flask run
   ```

## Usage

1. Open your browser and navigate to [http://localhost:5173](http://localhost:5173) (or your configured port).
2. Use the interface to either:
   - Enter your lyrics
   - Select a musical style
3. Click the **Generate** button to create your music. Your song will be generated using the backend APIs integrating YuE, ChatGPT, and Stable Diffusion.
4. Enjoy your custom AI-generated track and thumbnail!

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
