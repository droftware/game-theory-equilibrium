# Author: Akshat Tandon 201503001

import sys

def increment_profile(profile, playerStrategies, ignore = None):
	newProfile = list(profile)
	n = 1
	for i in range(len(playerStrategies)):
		if ignore != None and (ignore-1) == i:
			continue
		value = newProfile[i] + 1
		if value == (playerStrategies[i] + 1):
			newProfile[i] = 1
		else:
			newProfile[i] = value
			break
	return tuple(newProfile)

def find_equilibrium(playerStrategies, matrix, strong = True):
	dominant = [] #this vector stores the dominant strategy equilibrium
	for player in range(len(playerStrategies)):
		# print '-' * 20
		# print 'Player: ',player+1
		dominant.append(-1)
		profile = (1,) * len(playerStrategies)
		firstFlag = True
		moreStrategies = True
		probableDominants = []

		# loop for changing player strategies
		while moreStrategies:
			maxUtility = 0
			# print ' '
			# finds the max utility 
			prevProfile = profile
			for i in range(1, playerStrategies[player]+1):
				profileList = list(profile)
				profileList[player] = i 
				profile = tuple(profileList)
				utility = matrix[profile][player]
				# print 'Evaluating strategy profile: ', profile, ' Utility = ', utility
				if i == 1 or utility > maxUtility:
					# print 'Setting max utility, prev value= ', maxUtility, ' new value = ', utility
					maxUtility = utility

			# finds strategies which have this maxUtility
			# print ' '
			maxStrategies = []
			for i in range(1, playerStrategies[player]+1):
				profileList = list(profile)
				profileList[player] = i
				profile = tuple(profileList)
				if maxUtility == matrix[profile][player]:
					# print 'Strategy having max utility =',maxUtility,' is :', i
					maxStrategies.append(i)

			profile = increment_profile(prevProfile, playerStrategies, player+1)
			# print 'New profile: ', profile
			if profile == (1,) * len(playerStrategies):
				moreStrategies = False

			# depending on max utility , decide on dominant strategy
			if strong:
				# print 'Strong Dominant Equilibrium'
				if len(maxStrategies) != 1:
					# print 'Num max strategies not 1'
					dominant[player] = -1
					break
				if firstFlag:
					firstFlag = False
					# print 'First flag made false'
					dominant[player] = maxStrategies[0]
					# print 'Setting dominant[player] = ', maxStrategies[0]
				else:
					if dominant[player] != maxStrategies[0]:
						# print 'strategy mismatch ', dominant[player],' : ',maxStrategies[0]
						dominant[player] = -1
						break
			else:
				# print 'Weak Dominant Equilibrium'
				if len(probableDominants) == 0:
					# print 'Copying first set of strategies: ', maxStrategies
					probableDominants = maxStrategies[:]
				else:
					# print 'Before intersection:', probableDominants,' : ',maxStrategies
					setDominants = set(probableDominants).intersection(maxStrategies)
					probableDominants = list(setDominants)
					# print 'After intersection:', probableDominants
					if len(probableDominants) == 0:
						# print 'weak equilibrium not possible since NULL intersection'
						dominant[player] = -1
						break
					if moreStrategies == False:
						# print 'last set of comparisons'
						if len(probableDominants) != 1:
							# print 'inequality condition not satisfied, weak equilibrium not possible'
							dominant[player] = -1
							break
						else:
							# print 'inequality condition satisfied, setting equilibirum', probableDominants[0]
							dominant[player] = probableDominants[0]
			
		if dominant[player] == -1:
			# print 'XX Equilibrium does not exist XX'
			return None

	return dominant


def main():
	if len(sys.argv) != 2:
		print 'Correct Usage: equilibrium.py sample.nfg'
		sys.exit(0)
	fileName = sys.argv[1]
	title = ''
	playerNames = []
	playerStrategies = []
	matrix = {}
	f = open(fileName, 'rU')
	for line in f:
		line = line.strip()
		if len(line) == 0:
			print line
		else:
			if line[0] =='N':
				line = line.split()
				title = ' '.join(line[3:])
				# print 'Title is',title
			elif line[0] == '{':
				idx = line.find('}')
				plist = line[1:idx].split('"')
				for player in plist:
					player = player.strip()
					if len(player) != 0:
						playerNames.append(player)
				# print 'Players: ', playerNames
				remaining = line[idx:]
				idx = remaining.find('{')
				playerStrategies = remaining[idx+1:-1].split()
				numStrategies = 1
				for i in range(0,len(playerStrategies)):
					playerStrategies[i] = int(playerStrategies[i])
					numStrategies = numStrategies * playerStrategies[i]
					# print 'Strategy: ',playerStrategies[i]
			else:
				profile = (1,) * len(playerStrategies)
				i = 0
				utilities = line.split()
				print 'Strategy Profile -> Player utilities'
				while i < len(playerStrategies)*numStrategies:
					# print 'i=',i
					sts = []
					for j in range(len(playerStrategies)):
					# Converting to ints only, handle for floats also
						sts.append(int(utilities[i+j]))
					i += len(playerStrategies)
					matrix[profile] = tuple(sts)
					print profile,' -> ', matrix[profile]
					profile = increment_profile(profile, playerStrategies)

	assert(len(playerNames) == len(playerStrategies))
	f.close()
	print ' '
	dom = find_equilibrium(playerStrategies, matrix, True)
	if dom != None:
		print 'Strong dominant equilibirum: ', dom
	else:
		print 'Strong dominant equilibirum does not exist'

	dom = find_equilibrium(playerStrategies, matrix, False)
	if dom != None:
		print 'Weak dominant equilibirum: ', dom
	else:
		print 'Weak dominant equilibirum does not exist'



if __name__=='__main__':
	main()