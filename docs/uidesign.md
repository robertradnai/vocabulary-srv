# Basic UI design
This document aims to help the app design process by enabling quick prototyping of the user interface.

Forms, sites and components:
* Welcome site for unregistered users
* Welcome site for users that are logged in
* Own word lists
* Shared word lists
* Send feedback

Quiz:  
* Quiz starter site
* Flashcard
* Multiple choice quiz
* Statistics site
* End of quiz site?

## Front page without logging in

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
___
German - English  
**Workplace**  
[Start learning]()
___
Finnish - English  
**Basics I**  
[Start learning]()
___
## Front page with logged in user

### Remarks

* Show the users' cloned word lists.
* Later, maybe also some statistics about how many words they learned 
  and how many times they logged in in the last n days.

## Choose word lists to clone

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

## User word lists

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
German - English  
**Workplace**   
Progress: 75%   
Cloned at: 12 Jan 2021  
Last opened at: 12 Feb 2021  
[Start learning]() | [Assessment quiz]()  
[Reset learning progress]() | [Delete list]()  
___
Finnish - English  
**Basics I**  
Progress: 43%  
Cloned at: 12 Jan 2021  
Last opened at: 12 Feb 2021  
[Start learning]() | [Assessment quiz]()  
Manage (dropdown menu):
* [Reset learning progress]()
* [Delete list]()  
___

## Choose quiz type

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

## Flashcard

### Content

Finnish - English / Basics | [Back to list choice](#)

FINNISH  
> talo  

ENGLISH  
> house  

Remarks:  
> Some remarks

[Next](#) | 1/10 | 0% overall

***

German - English / Basics | [Back to list choice](#)

Das Wort
> Zimmer

Welcher ist der richtige Artikel?
> [der](#)   
> [die](#)  
> [das](#)  
  

[Next](#) | 6/10 | 3.5% overall

***

lang1 - lang2 / Word list name | [Back to list choice](#)

INSTRUCTION HEADER
> Instruction content

CHOICES HEADER
> [choices[0]](#)   
> [choices[1]](#)  
> [choices[2]](#)  

***

## Quiz

### Content

Finnish - English / Basic | [Back to list choice](#)

English
> Room

Finnish - how would you translate it?
> paita  
> huone  
> haave  
> ottaa  

[Next](#) | 6/10 | 3.5% overall