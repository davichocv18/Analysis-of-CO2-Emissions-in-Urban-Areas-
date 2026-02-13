# 🚗 Traffic Simulation and CO₂ Emissions Estimation using SUMO and Machine Learning

This repository contains the full implementation of a research project focused on traffic simulation, dataset generation, and CO₂ emissions estimation using microscopic traffic simulations and machine learning models.

The project was developed as part of an academic research study and later published in an international conference proceedings.

📄 Published paper: https://link.springer.com/chapter/10.1007/978-3-032-08366-1_17

## 📂 Content

- **Simulation scripts** 🛠️
Source code used to generate and analyze simulations.

- **Generated dataset** 📊  
  Data used for model training and validation.

- **Web application in Streamlit** 🌐  
  Interactive interface that allows you to visualize and test the model.

- **Trained model** 🤖  
  Model file ready to be used in the application.

Each folder contains its own README with detailed instructions on how to run the corresponding components.

## 🚦 Project Overview

This project presents a complete framework for analyzing and predicting carbon dioxide (CO₂) emissions in urban areas by combining traffic microsimulation and machine learning techniques.

The study focuses on an urban area of Quito, Ecuador (Historic Center) and uses the SUMO (Simulation of Urban Mobility) simulator to generate realistic traffic data. Based on these simulations, a large synthetic dataset is created and used to train machine learning models capable of predicting total and disaggregated CO₂ emissions under different traffic densities and vehicle distributions.

The final outcome is an interactive web application that allows users to estimate emissions without running computationally expensive simulations, making the solution scalable and practical for decision-making.

## 🎯 Objectives

- Simulate realistic urban traffic scenarios using SUMO
- Model vehicle behavior based on Ecuadorian fleet data
- Estimate CO₂ emissions under different traffic densities
- Build a robust dataset from large-scale simulations
- Train machine learning models to predict emissions
- Deploy an interactive web application for public use

## 🧠 Methodology Summary

The methodology is divided into three main stages:

- Calibration and Traffic Simulation (SUMO)
- Dataset Generation and Analysis
- Machine Learning Production

## 🖥️ Computational Resources

Due to the high cost of simulations and data processing:
Dataset generation required ~2 weeks of continuous execution
High-performance server used:

- CPU: AMD EPYC 7702P
- Cores: 128
- RAM: 1 TB
- OS: Ubuntu 20.04 LTS

## 🌐 Web Application

The final model is deployed using Streamlit, allowing users to:

- Adjust vehicle density and distribution
- Instantly predict CO₂ emissions
- Visualize results with charts
- Export results as: CSV (raw data),  Excel (data + charts), PDF (summary report)

## 🤝 Contact
If you have questions, feedback, or collaboration proposals, feel free to reach out.
David Casa
ICT Researcher | Machine Learning | Urban Mobility & Emissions
v.david1804@gmail.com

##📜 License & Usage

© All rights reserved.

This project, including its code, datasets, and trained models, is the intellectual property of the author.

The code is provided for academic, research, and evaluation purposes only.

Any reuse, modification, or redistribution of this project or its components must be explicitly authorized by the author.

If you are interested in using this work for research, commercial, or academic purposes, please contact the author first.



