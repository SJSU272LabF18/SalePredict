# Project Team-27

## Student Names: 
Shreyam Kela,
Harsh Agarwal,
Vaishali Koul,
Sayalee Shankar Bhusari

## Team Name: Phoenix

### Approved Project Idea: Will It Sell? - Mobile Application Success Prediction System

Description: Ever made an app that got you pulling all-nighters for weeks, only to get the lowest possible ranking on the app store? Feels terrible, right? Next time you build an app, use this prediction system to assess the success of your app before you start banging away at your keyboard to get that app on the app store. Our prediction system analyses the app description you provide and it provides you back with the detailed analysis of your app's potential selling quotient. With the help of this detailed report, the app developers can adapt their app with respect to the market trend, so as to increase the selling ability of the app.


Methodology: 

- Prediction systems are rooted on logic-based deductions. In the ideal case, all the apps that are very similar should perform equally on the app store. This is the fundamental idea behind our prediction model. 
- As we include real world constraints such as age-group focus area, geographical focus area, app size, and so on, into the model, it gets closer to the actual market performance. 
- To find the similar descriptions, we apply Natural Language Processing on the App Store dataset to find the Nearest Neighbours of the new description entered, using TFIDF of the descriptions in the dataset and their Cosine Similarities with respect to the new description.
- Our system analyses the new description entered and determines the detailed analysis such as the potential app store rating, total number of installs, top similar apps, and so on.
- The NLP model is served through a Flask Server at the Back-end and the detailed report is rendered on the web interface with the help of ReactJS at the Front-end. 
- The *nlp_engine* folder contains the Natural Language Processing Model and the Flask Server program files, while the *ReactFrontend* folder contains the ReactJS Web Interface program files, that talk to the Flask Server.


Dataset: https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps

Professor's Comment: I would also predict key metrics such as number of downloads by geography and age group etc.. 

Design Mockup: https://invis.io/C7P3GP56X5K
