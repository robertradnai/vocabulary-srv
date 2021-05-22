# Basic UI design
This document aims to help the app design process by enabling quick prototyping of the user interface.

Forms, sites and components:
* Welcome site for unregistered users (intro text + available word lists)
* Welcome site for users that are logged in (--> own word lists)
* My word lists
* Available word lists
* Send feedback

Quiz:  
* Quiz starter site before first quiz round
* Statistics site between quiz rounds
* End of quiz site
* Flashcard
* Multiple choice quiz


## Welcome site for unregistered users 

### Remarks
* The user type should be communicated to the front end because some app functionalities
  depend on whether we are a normal or a guest user (e. g. start learning and add 
  to my lists button)

### Content

This application is being built to help you learn foreign words 
faster by guiding you through flashcards and quizes in an adaptive manner. 
You can already try it with the word lists below, and soon, you'll be able to 
save your progress and edit your own word lists. 

[**REGISTER**]()

Or start a demo:  
> Same content here as shared lists site

## Welcome site for users that are logged in

### Remarks

* Show the users' cloned word lists.
* Later, maybe also some statistics about how many words they learned 
  and how many times they logged in in the last n days.

### Content
> Same as user word lists site

## My word lists

### Remarks 
* When the language direction is inverted, does that still count as additional learning progress?
* How valuable is this switch languages function?
  * Maybe it depends on which language the learner wants to learn 
    (German native speaker learning Hungarian or Hungarian native speaker learning German).
  * But then most of the remarks are useless, one knows their native language well enough
  * *7 March 2021: It's decided that the language direction change won't be implemented
    in the near future due to low added value*

### Content
___
German (for English speakers)  
**Workplace**   
Progress: 75%   
Cloned at: 12 Jan 2021  
Last opened at: 12 Feb 2021  
[Start learning]() | [Assessment quiz]()  
[Reset learning progress]() | [Delete list]()  
___
Finnish (for English speakers)   
**Basics I**  
Progress: 43%  
Cloned at: 12 Jan 2021  
Last opened at: 12 Feb 2021  
[Start learning]() | [Assessment quiz]()  
Manage (dropdown menu):
* [Reset learning progress]()
* [Delete list]()  
___

## Available word lists

### Content

Order by: [most popular]() | [newest]()  
Filter word lists: ________ | [Apply]()
___
German - English  
**Workplace**  
[Add to my lists]() | [Start learning]()
___
Finnish - English  
**Basics I**  
Already added | [Continue learning]()
___



## Future user list site - Quiz type choice

### Remarks
* Not all lists are suitable for all quiz types
* How will the learning progress be registered in the other quiz types?  
  Completing a quiz about articles doesn't mean that the user knows the words -->
  Separated learning progress per quiz type? 
* If a word list contains verbs and nouns as well, and we'd like to run a 
  quiz for der/die/das articles, then we need to pre-filter the word list
  so that it only contains nouns with articles. Regexp is a good for a 
  first try but are there 
  more complicated filtering needs?

### Content
___
German - English  
**Workplace**   
Progress: 75%   
Cloned at: 12 Jan 2021  
Last opened at: 12 Feb 2021  
[Start learning]() | [Assessment quiz]()  
Extra quizzes:
* [Präpositions]()
* [Definitiv Artikel]()  

Manage (dropdown menu):
* [Reset learning progress]()
* [Delete list]()  
___

## Quiz - Quiz starter site before first quiz round

### Remarks

### Content

Finnish (for English speakers) / Basics | [Back to my word lists](#)  

In this quiz round, you'll see
* a few flashcards, try to memorize them,
* questions based on the new flashcards,
* and questions based on earlier flashcards to deepen your knowledge.

Your learning progress will be saved after each finished quiz round.

## Quiz - Statistics site between quiz rounds

### Remarks

### Content

Finnish (for English speakers) / Basics | [Back to my word lists](#)

You answered 4 out of the 5 questions correctly.

Your learning progress on the whole list: 13.3 %

## Quiz - End of quiz site

### Remarks

### Content

Finnish (for English speakers) / Basics | [Back to my word lists](#)

*Congratulations!* You've just finished this word list by 
repeatedly answering the quiz questions correctly.

## Quiz - Flashcard

### Content

Finnish (for English speakers) / Basics 1 | [Back to my word lists](#)

FINNISH  
> talo  

ENGLISH  
> house  

Remarks:  
> Some remarks

[Next](#) | 1/10 | 0% overall

***

German (for English speakers) / Basics | [Back to my word lists](#)

Das Wort
> Zimmer

Welcher ist der richtige Artikel?
> [der](#)   
> [die](#)  
> [das](#)  
  

[Next](#) | 6/10 | 3.5% overall

***

lang1 (for lang2 speakers) / Word list name | [Back to my word lists](#)

INSTRUCTION HEADER
> Instruction content

CHOICES HEADER
> [choices[0]](#)   
> [choices[1]](#)  
> [choices[2]](#)  

***

## Quiz - Multiple-choice quiz

### Content

Finnish (for English speakers) / Basics 1 | [Back to my word lists](#)

English
> Room

Finnish - how would you translate it?
> paita  
> huone  
> haave  
> ottaa  

[Next](#) | 6/10 | 3.5% overall