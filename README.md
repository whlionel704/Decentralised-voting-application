# voting_app

In this repository, the smart contract represents a decentralised voting application. This is referenced from an existing voting application in the following link: https://developer.algorand.org/articles/creating-stateful-algorand-smart-contracts-python-pyteal/. 

The pyteal code in the smart contract is specifically targeting the following real life application: Suppose a boss of a company wants to create a new company logo. There are only 3 possible colours to choose from. It is either red, yellow or blue. The boss wants a certain number of employees to allocate a score of 10 to be distributed among the 3 colours. For example, an employee could give the scores as follows:- Red: 2, Yellow: 3, Blue: 5. The colour with the highest sum of scores among the employees will be the chosen colour for the new logo. To illustrate this, assume a 2nd employee votes for Red: 7, Yellow: 2, Blue: 1. If the boss only allowed a maximum of 2 employees to vote, then red will be the final chosen colour for the new logo because it has a score of 2+7=9, which is higher than yellow (3+2=5) and blue (5+1=6).


Let's now relate this real life scenario to the functions written in the Pyteal smart contract. 


Approval Program:-
 on_creation: Initialises the following global states:
 -- creator's identity
 -- start and end times for registration and voting respectively
 -- The initial scores for each of the 3 colours, which are equal to 0
 -- total number of employees allowed to participate in the voting

 update_timeFrame: Allows the boss to start a new voting process again, by setting new values for the start and end times

 on_closeout: Removes the scores of an employee who opts out before the voting has ended

 update_scores: Allows an employee to change his or her scores for the 3 colours as long as the voting has not ended yet

 on_register: This function will run when an employee opts in

 on_vote: This function will run when an employee assigns his or her scores to each of the 3 colours


Clear State Program:-
  Just like the on_closeout This will allow the employee to opt out. But the main difference is that the transaction records of that employee will be erased.


Some distinctive features of this smart contract:
 1.update_timeFrame function 
 2.update_scores function
 3.global state to track the total number of users which have voted. This ensures that we cannot have more voters than the specified maximum number of voters as initialised in the global state: Bytes("TotalUsers").
 4.Instead of simply voting for 3 colours, each employee is given a score of 10 to be distributed among the 3 colours in any way he or she wants.
 
 This smart contract also comes with a frontend user interface. Using the same application ID and by following the instructions in the 'README.md' file inside the 'Front-end interface' folder of this repository, it allows an employee to connect his or her perawallet to take part in the voting process in a user-friendly way.