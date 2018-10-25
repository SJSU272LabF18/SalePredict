# Project Team-27

## Student Names: 
Shreyam Kela,
Harsh Agarwal,
Vaishali Koul,
Sayalee Shankar Bhusari

## Team Name: Pheonix

### Project Idea 1: SalePoint - Best place to buy from during Black Friday

Every year during the Black Friday sale a horde of people line up outside the stores, hoping to get the best deal of their lives. Most of these people are left confused on seeing the humongous list of options where they might possibly find the product they desire, at *gauranteed* lowest price. In all the fuss, the product runs out of stock, and they miss the chance to even buy that article. Our proposed model takes training data of Black Friday prices and shopping trends from previous years, so as to decide which store would fetch potentially the best price this year, according to the previous trends. Our model would also take into account that the store selling the product at the lowest price could be selling fake/expired products. Therefore after training, the model should be able to predict the store where one can find the product at the lowest possible price with reasonable quality, if not the best. When the user inputs an item they want to purchase, the model would recommend stores and also preview previous ratings and reviews so that the user can make the final call.

Methodology: Dataset is analysed to determine the price trends for the product being searched for. Sentiment analysis is carried out on product descriptions and corresponding reviews so as to derive the places with best reviews. The dataset analysis is combined with the reviews analysis and HighCharts is used to graphically present to the user, the best possible store for the searched product.

Data set: The project can be accomplished by using opensource Black Friday Datasets.
For example: https://www.kaggle.com/mehdidag/black-friday



### Project Idea 2: Will It Sell? - Android App Success Predictor

Ever made an app that got you pulling all-nighters for weeks, only to get the lowest possible ranking on the app store? Feels terrible, right? Next time you build an app, use this prediction system to assess the success of your app before you start banging away at your keyboard to get that app on the app store. Our prediction system applies sentiment analysis on the app description you provide and it provides you back with a detailed analysis of your app's potential selling quotient.

Methodology: Apply SVM on the Google App Store dataset based on attributes like high rating, good reviews, large number of downloads, and so on. When the user inputs their proposed app description, our system determines the probable outcome as success or failure and the detailed analysis.

Dataset: https://www.kaggle.com/lava18/google-play-store-apps



### Project Idea 3: TakeMeHome! - A Ride Companion App
Attacks on students while traveling back home from campus are frequent. Being from different majors and having different lecture timings, it gets difficult for the students to travel in groups, even when they live on the same route. The app will help match them to other users AKA *travel companions*, any time of the day, based on their route. Before they choose to start off together, users would be able to assess the matched companion's credibility based on their ratings. As an added security measure, only users with an edu id will be able to sign up for the service. APIs of VTA-Transit/Uber/etc would be attached, for companions that use some mode of transport on their way.



### Project Idea 4: Gimme - A Food Sharing App
Leftovers can be a big problem. Post the details of your leftovers or the food that you bought but dont need, and you'll be surprised by the number of people that would happily take it. Share food for free or put your own price on it. Food sharers have to mention the expiry date of the food they're posting. Sharers get rated by the takers on the quality of shared food. Food is to be picked within a specified time.



### Project Idea 5: Sarcasm Detection
One of the most intriguing features of human discourse is Sarcasm. *"Alexa! Could you be any less audible?"* - your Alexa would have a hard time processing this statement. Statements rich in sarcasm or irony can only be detected mechanically when provided with context or by indentifying the overly positive or negative parts in any dialogue. Machine detection of such features is far from perfect, and there is a lot of scope for improvement in this area of Sentiment Analysis. The project aims to create a framework for efficient detection of sarcasm in feeds from Twitter, by the analysis of context and identification of double positives or negatives in the statements.
