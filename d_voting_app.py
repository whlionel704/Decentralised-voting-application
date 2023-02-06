#This smart contract automates a decentralised voting application. It is an improvement from the voting app smart contract 
#which can be found in the following website: https://developer.algorand.org/articles/creating-stateful-algorand-smart-contracts-python-pyteal/

#Last used App id from the testnet: 156791600

from pyteal import *

def approval_program():
    #This will initialise all the global variables right from the start
    on_creation = Seq([
        App.globalPut(Bytes("Creator"), Txn.sender()),
        Assert(Txn.application_args.length() == Int(8)),
        App.globalPut(Bytes("RegBegin"), Btoi(Txn.application_args[0])),
        App.globalPut(Bytes("RegEnd"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("VoteBegin"), Btoi(Txn.application_args[2])),
        App.globalPut(Bytes("VoteEnd"), Btoi(Txn.application_args[3])),
        App.globalPut(Bytes("TotalUsers"), Btoi(Txn.application_args[4])),
        App.globalPut(Bytes("TotalCountRed"), Btoi(Txn.application_args[5])),
        App.globalPut(Bytes("TotalCountYellow"), Btoi(Txn.application_args[6])),
        App.globalPut(Bytes("TotalCountBlue"), Btoi(Txn.application_args[7])),
        Return(Int(1))
    ])

    #Define the creator
    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))

    #initialise the color choices #enter each --app-arg as an integer
    choiceRed = Btoi(Txn.application_args[1])
    choiceYellow = Btoi(Txn.application_args[2])
    choiceBlue = Btoi(Txn.application_args[3])

    #get the total scores for each of the 3 colors
    choice_tally_Red = App.globalGet(Bytes("TotalCountRed")) 
    choice_tally_Yellow = App.globalGet(Bytes("TotalCountYellow"))
    choice_tally_Blue = App.globalGet(Bytes("TotalCountBlue"))

    #use local state to check whether user voted or not
    voted_or_not = App.localGetEx(Int(0), App.id(), Bytes("voted"))

    #This function will allow the app creator to update the timeframes to start a new voting process as soon as the voting period is over
    update_timeFrame = Seq([
        Assert(Global.latest_timestamp() >= App.globalGet(Bytes("VoteEnd"))),
        App.globalPut(Bytes("RegBegin"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("RegEnd"), Btoi(Txn.application_args[2])),
        App.globalPut(Bytes("VoteBegin"), Btoi(Txn.application_args[3])),
        App.globalPut(Bytes("VoteEnd"), Btoi(Txn.application_args[4])),
        Assert(Txn.sender() == App.globalGet(Bytes("Creator"))),
        Return(Int(1))
    ])

    #This function will run if the voter chooses to quit before the voting period ends
    on_closeout = Seq([
        voted_or_not,
        If(And(voted_or_not.hasValue(), Global.latest_timestamp() <= App.globalGet(Bytes("VoteEnd"))), Seq([
            App.globalPut(Bytes("TotalCountRed"), App.globalGet(Bytes("TotalCountRed")) - App.localGet(Int(0), Bytes("votedRed"))),
            App.globalPut(Bytes("TotalCountYellow"), App.globalGet(Bytes("TotalCountYellow")) - App.localGet(Int(0), Bytes("votedYellow"))),
            App.globalPut(Bytes("TotalCountBlue"), App.globalGet(Bytes("TotalCountBlue")) - App.localGet(Int(0), Bytes("votedBlue"))),
            App.globalPut(Bytes("TotalUsers"), App.globalGet(Bytes("TotalUsers")) + Int(1)),
        ])),
        Return(Int(1))
    ])

    #This function will allow the voter to modify the scores assigned to each color. 
    #The voter is free to modify his scores as long as the voting period is still ongoing.
    update_scores = Seq([
        voted_or_not,
        If(And(voted_or_not.hasValue(), Global.latest_timestamp() <= App.globalGet(Bytes("VoteEnd"))), Seq([
            App.globalPut(Bytes("TotalCountRed"), App.globalGet(Bytes("TotalCountRed")) - App.localGet(Int(0), Bytes("votedRed"))),
            App.localPut(Int(0), Bytes("votedRed"), Btoi(Txn.application_args[1])),
            App.globalPut(Bytes("TotalCountRed"), App.globalGet(Bytes("TotalCountRed")) + App.localGet(Int(0), Bytes("votedRed"))),

            App.globalPut(Bytes("TotalCountYellow"), App.globalGet(Bytes("TotalCountYellow")) - App.localGet(Int(0), Bytes("votedYellow"))),
            App.localPut(Int(0), Bytes("votedYellow"), Btoi(Txn.application_args[2])),
            App.globalPut(Bytes("TotalCountYellow"), App.globalGet(Bytes("TotalCountYellow")) + App.localGet(Int(0), Bytes("votedYellow"))),

            App.globalPut(Bytes("TotalCountBlue"), App.globalGet(Bytes("TotalCountBlue")) - App.localGet(Int(0), Bytes("votedBlue"))),
            App.localPut(Int(0), Bytes("votedBlue"), Btoi(Txn.application_args[3])),
            App.globalPut(Bytes("TotalCountBlue"), App.globalGet(Bytes("TotalCountBlue")) + App.localGet(Int(0), Bytes("votedBlue"))),
        ])),
        Return(Int(1))
    ])

    #This function will run when the voter opts in
    on_register = Seq([
        Return(And(Global.latest_timestamp() >= App.globalGet(Bytes("RegBegin")),
        Global.latest_timestamp() <= App.globalGet(Bytes("RegEnd"))))
    ])

    #This function will run during the voting period
    on_vote = Seq([
        #makes sure that the current round is within the voting period
        Assert(And(
            Global.latest_timestamp() >= App.globalGet(Bytes("VoteBegin")),
            Global.latest_timestamp() <= App.globalGet(Bytes("VoteEnd"))
        )), 
        voted_or_not,        

        #the total score for the 3 colors must be equal to 10
        Assert(choiceRed + choiceYellow + choiceBlue == Int(10)),

        #Makes sure that the user has not voted yet. This avoids double voting
        If(voted_or_not.hasValue(), Return(Int(0))),
        
        App.globalPut(Bytes("TotalCountRed"), choice_tally_Red + choiceRed), 
        App.localPut(Int(0), Bytes("votedRed"), choiceRed), 
        App.globalPut(Bytes("TotalCountYellow"), choice_tally_Yellow + choiceYellow), 
        App.localPut(Int(0), Bytes("votedYellow"), choiceYellow), 
        App.globalPut(Bytes("TotalCountBlue"), choice_tally_Blue + choiceBlue), 
        App.localPut(Int(0), Bytes("votedBlue"), choiceBlue), 


        #update local state - the user has already voted
        App.globalPut(Bytes("TotalUsers"), App.globalGet(Bytes("TotalUsers")) - Int(1)),
        App.localPut(Int(0), Bytes("voted"), Int(1)),
        Return(Int(1))
    ])

    #main conditional
    program = Cond(
        [Txn.application_id() == Int(0), on_creation], 
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_register],
        [Txn.application_args[0] == Bytes("updated_tf"), update_timeFrame],
        [Txn.application_args[0] == Bytes("update_scores"), update_scores],
        [Txn.application_args[0] == Bytes("vote"), on_vote]
    )
    
    return compileTeal(program, Mode.Application, version=5)
    

def clear_state_program():
    voted_or_not = App.localGetEx(Int(0), App.id(), Bytes("voted"))
    choiceRed = Btoi(Txn.application_args[1])
    choiceYellow = Btoi(Txn.application_args[2])
    choiceBlue = Btoi(Txn.application_args[3])

    program = Seq([
        voted_or_not,
        If(And(voted_or_not.hasValue(), Global.latest_timestamp() <= App.globalGet(Bytes("VoteEnd"))), Seq([
            App.globalPut(Bytes("TotalCountRed"), App.globalGet(Bytes("TotalCountRed")) - App.localGet(Int(0), Bytes("votedRed"))),
            App.globalPut(Bytes("TotalCountYellow"), App.globalGet(Bytes("TotalCountYellow")) - App.localGet(Int(0), Bytes("votedYellow"))),
            App.globalPut(Bytes("TotalCountBlue"), App.globalGet(Bytes("TotalCountBlue")) - App.localGet(Int(0), Bytes("votedBlue"))),
            App.globalPut(Bytes("TotalUsers"), App.globalGet(Bytes("TotalUsers")) + Int(1)),
        ])),

        Return(Int(1))
    ])

    return compileTeal(program, Mode.Application, version=5)

appFile = open('approval.teal','w')
appFile.write(approval_program())
appFile.close()

clearFile = open('clear.teal','w')
clearFile.write(clear_state_program())
clearFile.close()

print(approval_program())
print(clear_state_program())