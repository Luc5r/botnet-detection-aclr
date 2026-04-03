# 🤖 Hybrid Deep Learning Model for Botnet Detection in IoT

![Python](https://img.shields.io/badge/Python-3.x-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepLearning-orange)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)
![Domain](https://img.shields.io/badge/Domain-Cybersecurity-red)

---

## 📌 Overview

This project presents a **hybrid deep learning model (ACLR)** for detecting botnet attacks in IoT environments. By combining multiple neural networks, the system improves detection accuracy and adapts to evolving cyber threats.

---

## ⚠️ Problem Statement

Traditional intrusion detection systems fail to detect **unknown and evolving botnet attacks** in IoT networks due to limited pattern recognition and high false positives.

---

## 💡 Proposed Solution

A **stacked hybrid model (ACLR)** combining:

* 🧠 ANN → Complex feature learning
* 🧩 CNN → Spatial pattern extraction
* ⏳ LSTM → Temporal dependency learning
* 🔁 RNN → Sequential behavior modeling

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Network Traffic Input]

    A --> B[ANN]
    A --> C[CNN]
    A --> D[LSTM]
    A --> E[RNN]

    B --> F[Stacking Layer ACLR]
    C --> F
    D --> F
    E --> F

    F --> G[Final Prediction]
    G --> H[Botnet / Normal]
```

---

## 📊 Dataset

* UNSW-NB15 dataset
* Includes multiple attack types:

  * Normal
  * DoS
  * Exploits
  * Fuzzers
  * Reconnaissance
  * Backdoor
  * Shellcode
  * Worms

---

## ⚙️ Methodology

1. Data preprocessing & normalization
2. Train ANN, CNN, LSTM, RNN models
3. Combine models using stacking (ACLR)
4. Evaluate using:

   * Accuracy
   * Precision
   * Recall
   * ROC-AUC

---

## 📈 Results

* ✅ Accuracy: ~96–99%
* ✅ Strong multi-class classification
* ✅ Improved detection of unknown attacks
* ✅ Reduced false positives

---

## 🚀 How to Run

```bash
python frontend.py
```

---

## 🧰 Tech Stack

* Python
* TensorFlow / Keras
* Scikit-learn
* Pandas, NumPy

---

## ✨ Key Features

* Hybrid deep learning architecture
* Multi-class botnet detection
* Scalable for IoT environments
* Handles evolving cyber threats

---

## 🔮 Future Work

* Real-time deployment
* Integration with IDS systems
* Lightweight model optimization

---

## 👨‍💻 Author

**Satya Sai**
B.Tech Computer Science and Engineering (Cyber Security)

---

## 📌 Note

Large dataset and model files are managed using Git LFS due to GitHub size limitations.
