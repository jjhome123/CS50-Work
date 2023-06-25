# Project Name: English Word List Compatibility Checker
## Period [ 2023 February 17 ~ Present ]
## URL: https://www.youtube.com/watch?v=vnx5Cu5U-h0

### *** Background ***
In Japanese public high schools, many English teachers manually cross reference authentic English texts with large word lists provided to them by their school or board of education. The issue here is that this process can take a very long time, especially when a teacher wants to go through a larger text or many shorter texts.

### *** Project Overview ***
For my CS50 Final Project, I created a web application that attempts to solve this problem. It cross-references each word in a string of text with an SQLite database loaded with the official Hyogo Prefecture standard for middle-school vocabulary. After cross-referencing, this program displays the words that were not found in the vocabulary list to an HTML page created with Flask/Jinja. Furthermore, these words are compared to a different database containing word-synonym pairs. Matches here return synonyms to the HTML page in table-format.

### *** Considerations/Reflections ***
- This project's initial goal was to simply display the user's raw input and a list of words from the input that were not found in the word list. However, as more time was spent working on the project, I began to think of ideas for new features that would make the application more user-friendly or helpful.

#### The Word Parser Algorithm
What I thought to be a simple task became very complicated, very quickly. Accepting words in their plural form, tense changes, contractions, etc. were suddenly issues that I had to resolve.

For example, "dog" would be in the word list but if "dogs" was in the input string, how would my program accept "dogs?" And if "dogs" was acceptable, how about "buzz" and "buzzes?" Creating an algorithm to account for these changes has left me with a certain degree of uncertainty as to whether I have accounted for all possible exceptions/anomalies in English.

#### The Synonyms Feature
The largest feature I added to my application was the synonyms feature. Initially, I thoguht to reference thesaurus data from an API by sending GET requests to a URL, as that was a method used in the CS50 Finance problem. However, I ran into two issues:

1. In the case of a large input string, odds were that the number of words not found in the word list was large. As a result, there would be hundreds of GET requests sent to the API, and this made the runtime of my application **extremely long.**
2. Another issue was that using an API was not free, and I was not willing to spend money for my project. Many of them had a daily limit of requests that could be made per day, if not paying for it. As one of my goals was to have many others use my application, I quickly realized that using an API from a website was probably out of the question.

After doing some research, I found a GitHub repository containing a synonym database from Princeton University's WordNet. By pulling a copy of this database to my local repository and referencing this data, I thought I could significantly reduce my application's runtime.