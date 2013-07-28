#!/usr/bin/python
import platonic
import sys
#Player naming is case insensitive. 
#Outputs the rate of victory, the average time of victory, the average 
#proportion of victory and the most victorious victory.
GameParams = platonic.gameParams()
scoreFile = "scores.log"
player = sys.argv[1]
playerData = [  [ [], [], [], [], 0 ], [ [], [], [], [], 1 ], [ [], [], [], [], 2], [ [], [], [], [], 3 ]  ]
for line in open (scoreFile, 'r'):
   name, modeNum, numSweeps, time = line.split()[0], int(line.split()[1]), int(line.split()[2]), float(line.split()[3])
   if name.lower() == player.lower(): 
      playerData[modeNum][0].append(numSweeps)
      playerData[modeNum][1].append(time)
      if modeNum == GameParams.EXPERT and numSweeps == GameParams.EXPERT_HEIGHT * GameParams.EXPERT_WIDTH - GameParams.EXPERT_BOMBCOUNT:
         playerData[modeNum][2].append(numSweeps)
         playerData[modeNum][3].append(time)
      elif modeNum == GameParams.DIFFICULT and numSweeps == GameParams.DIFFICULT_HEIGHT * GameParams.DIFFICULT_WIDTH - GameParams.DIFFICULT_BOMBCOUNT:
         playerData[modeNum][2].append(numSweeps)
         playerData[modeNum][3].append(time)
      elif modeNum == GameParams.REGULAR and numSweeps == GameParams.REGULAR_HEIGHT * GameParams.REGULAR_WIDTH - GameParams.REGULAR_BOMBCOUNT:
         playerData[modeNum][2].append(numSweeps)
         playerData[modeNum][3].append(time)
      elif modeNum == GameParams.EASY and numSweeps == GameParams.EASY_HEIGHT * GameParams.EASY_WIDTH - GameParams.EASY_BOMBCOUNT:
         playerData[modeNum][2].append(numSweeps)
         playerData[modeNum][3].append(time)

print "With seconds as a unit of time..."
for mode in playerData:
   if mode[4] == GameParams.EXPERT: 
      var = "Expert"
      n = GameParams.EXPERT_HEIGHT * GameParams.EXPERT_WIDTH - GameParams.EXPERT_BOMBCOUNT
   if mode[4] == GameParams.DIFFICULT: 
      var = "Difficult"
      n = GameParams.DIFFICULT_HEIGHT * GameParams.DIFFICULT_WIDTH - GameParams.DIFFICULT_BOMBCOUNT
   if mode[4] == GameParams.REGULAR: 
      var = "Regular"
      n = GameParams.REGULAR_HEIGHT * GameParams.REGULAR_WIDTH - GameParams.REGULAR_BOMBCOUNT
   if mode[4] == GameParams.EASY: 
      var = "Easy"
      n = GameParams.EASY_HEIGHT * GameParams.EASY_WIDTH - GameParams.EASY_BOMBCOUNT
   print "In " + var + " mode:"
   if len(mode[0]) > 0 and len(mode[2]) > 0:
      print("   Proportion of victorious games is : %.3f" % (len(mode[3]) / float(len(mode[1]))))
      print("   Average proportion of field swept is: %.3f" % (sum(mode[0]) / float(len(mode[0]) * n)))
      print("   Average time of victory is: %.3f" % (sum(mode[3]) / float(len(mode[3]))))
      print("   Swifest Victory is: %.3f" % min(mode[3]))
   else:
      print("   No wins yet")
